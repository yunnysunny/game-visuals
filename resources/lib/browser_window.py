import os
import threading
import time

import xbmc
import xbmcaddon
import xbmcgui

from .utils import get_game_info, log, play_rom
from .constants import ROM_EXTENSIONS, MEDIA_FOLDERS, ROM_DIR_INFO
from .detail_window import format_rating, show_game_detail

addon = xbmcaddon.Addon()

# 设置项 browse_layout 的取值 → 布局文件；0 表示使用 Kodi 默认列表，不打开自定义窗口
LAYOUT_XML = {
    1: "browser_classic.xml",
    2: "browser_hero.xml",
    3: "browser_wall.xml",
    4: "browser_retrotv.xml",
}

ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92
ACTION_SHOW_INFO = 11
ACTION_CONTEXT_MENU = 117

CONTROL_LIST = 50
# 焦点在同一个游戏上停留多久后开始播放预告片（秒）
PREVIEW_DELAY = 1.5
CART_LABEL_COUNT = 8


class GameBrowserWindow(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir_stack = [kwargs.get("rom_dir", "")]
        self.media_path = os.path.join(addon.getAddonInfo("path"), "resources", "skins", "default", "media")
        self.window_id = None
        self.preview = None  # 当前由本窗口启动的预告片路径
        self.closing = False
        self.detail_open = False
        self.hold_until = 0
        self.preview_started = 0
        self.preview_retries = 0
        self.preview_lock = threading.Lock()
        self.preview_thread = None

    @property
    def current_dir(self):
        return self.dir_stack[-1]

    def onInit(self):
        # 从游戏、详情页返回时也会再次调用 onInit，此时保留列表和选中位置
        self.window_id = xbmcgui.getCurrentWindowId()
        self.list_control = self.getControl(CONTROL_LIST)
        if self.list_control.size() == 0:
            self.load_dir(self.current_dir)
        self.setFocusId(CONTROL_LIST)
        if self.preview_thread is None:
            self.preview_thread = threading.Thread(target=self.preview_loop, daemon=True)
            self.preview_thread.start()

    def build_items(self, directory):
        game_info = get_game_info(directory)
        skip_media_folders = addon.getSettingBool("skip_media_folders")
        default_logo = os.path.join(addon.getAddonInfo("path"), "resources", "logos", "default.png")
        default_fanart = addon.getAddonInfo("fanart")
        rom_dirname = os.path.basename(directory).lower()
        platform = ROM_DIR_INFO.get(rom_dirname, {}).get("full_name", "")

        folders, games = [], []
        for name in os.listdir(directory):
            full_path = os.path.join(directory, name)
            if os.path.isdir(full_path):
                if not os.listdir(full_path):
                    continue
                if skip_media_folders and name.lower() in MEDIA_FOLDERS:
                    continue
                info = ROM_DIR_INFO.get(name.lower(), {"full_name": name})
                logo = os.path.join(addon.getAddonInfo("path"), "resources", "logos", f"{name.lower()}.png")
                if not os.path.exists(logo):
                    logo = default_logo
                li = xbmcgui.ListItem(label=info["full_name"])
                li.setArt({"thumb": logo, "icon": logo, "poster": logo})
                li.setProperty("isfolder", "true")
                li.setProperty("path", full_path)
                li.setProperty("title", info["full_name"])
                lang = xbmc.getLanguage(xbmc.ISO_639_1)
                li.setProperty("plot", info.get("description_zh", "") if lang == "zh" else info.get("description_en", ""))
                folders.append(li)
                continue
            if not name.lower().endswith(ROM_EXTENSIONS):
                continue
            meta = game_info.get(name, {})
            title = meta.get("title") or os.path.splitext(name)[0]
            thumb = meta.get("thumb") or meta.get("fanart") or default_logo
            li = xbmcgui.ListItem(label=title)
            li.setArt({
                "thumb": thumb,
                "poster": thumb,
                "icon": thumb,
                "fanart": meta.get("fanart") or default_fanart,
            })
            li.setProperty("path", full_path)
            li.setProperty("file", name)
            li.setProperty("title", title)
            li.setProperty("platform", platform)
            li.setProperty("plot", meta.get("plot", ""))
            li.setProperty("year", str(meta["year"]) if meta.get("year") else "")
            li.setProperty("genre", meta.get("genre", ""))
            li.setProperty("developer", meta.get("developer", ""))
            li.setProperty("publisher", meta.get("publisher", ""))
            li.setProperty("players", meta.get("players", ""))
            li.setProperty("rating", format_rating(meta.get("rating")))
            li.setProperty("trailer", meta.get("trailer") or "")
            games.append(li)

        folders.sort(key=lambda li: li.getLabel().lower())
        games.sort(key=lambda li: li.getLabel().lower())
        for i, li in enumerate(games):
            li.setProperty("cart_label", os.path.join(self.media_path, f"cart_label_{i % CART_LABEL_COUNT}.png"))
        return folders + games, platform, len(games)

    def load_dir(self, directory, select_path=None):
        try:
            items, platform, game_count = self.build_items(directory)
        except OSError as e:
            log(f"Error reading directory {directory}: {e}", xbmc.LOGWARNING)
            items, platform, game_count = [], "", 0
        self.setProperty("platform", platform or os.path.basename(directory.rstrip("\\/")))
        self.setProperty("count", addon.getLocalizedString(30336).format(game_count) if game_count else "")
        self.list_control.reset()
        self.list_control.addItems(items)
        position = 0
        if select_path:
            for i, li in enumerate(items):
                if li.getProperty("path") == select_path:
                    position = i
                    break
        if items:
            self.list_control.selectItem(position)

    def is_preview_playing(self):
        player = xbmc.Player()
        if not self.preview or not player.isPlayingVideo():
            return False
        return os.path.normcase(player.getPlayingFile()) == os.path.normcase(self.preview)

    def stop_preview(self):
        if self.is_preview_playing():
            xbmc.Player().stop()
        self.preview = None

    def is_busy(self):
        """详情页、弹窗、游戏或其它窗口在前台时不播放预告片"""
        return (self.detail_open
                or xbmcgui.getCurrentWindowId() != self.window_id
                or xbmc.getCondVisibility("System.HasModalDialog | Player.HasGame"))

    def hold_preview(self, seconds):
        """停止预告片，并在接下来 seconds 秒内不自动播放"""
        with self.preview_lock:
            self.hold_until = max(self.hold_until, time.time() + seconds)
            self.stop_preview()

    def preview_loop(self):
        """后台线程：焦点停留 PREVIEW_DELAY 秒后在 videowindow 中播放预告片"""
        monitor = xbmc.Monitor()
        last_path = None
        focused_since = time.time()
        while not self.closing and not monitor.waitForAbort(0.25):
            with self.preview_lock:
                now = time.time()
                if self.is_busy():
                    # 窗口切换有延迟，忙碌状态结束后再等 PREVIEW_DELAY 秒
                    self.hold_until = max(self.hold_until, now + PREVIEW_DELAY)
                if now < self.hold_until:
                    focused_since = now
                    continue
                path = xbmc.getInfoLabel(f"Container({CONTROL_LIST}).ListItem.Property(path)")
                if not path:
                    # 视频刚开始播放时 InfoLabel 可能短暂取不到值，不当作切换了选中项
                    continue
                if path != last_path:
                    last_path = path
                    focused_since = now
                    self.preview_retries = 0
                    self.stop_preview()
                    continue
                trailer = xbmc.getInfoLabel(f"Container({CONTROL_LIST}).ListItem.Property(trailer)")
                if trailer and trailer == self.preview:
                    # Kodi 刚结束 RetroPlayer 时打开视频偶尔会立即被关闭，启动失败时重试
                    started_ago = now - self.preview_started
                    if not xbmc.Player().isPlaying() and 1 < started_ago < 5 and self.preview_retries < 2:
                        log("Preview trailer failed to start, retrying")
                        self.preview_retries += 1
                        self.preview = None
                    continue
                if not trailer or now - focused_since < PREVIEW_DELAY:
                    continue
                # 用户自己在播放其它媒体时不打断
                if xbmc.Player().isPlaying() and not self.is_preview_playing():
                    continue
                log(f"Preview trailer: {trailer}")
                self.preview = trailer
                self.preview_started = now
                xbmc.Player().play(trailer, windowed=True)

    def open_detail(self, li):
        with self.preview_lock:
            self.detail_open = True
            self.stop_preview()
        try:
            show_game_detail(self.current_dir, li.getProperty("file"), os.path.basename(self.current_dir).lower())
        finally:
            self.detail_open = False

    def exit(self):
        self.closing = True
        self.stop_preview()
        self.close()

    def onAction(self, action):
        action_id = action.getId()
        if action_id in [ACTION_PREVIOUS_MENU, ACTION_NAV_BACK]:
            if len(self.dir_stack) <= 1:
                self.exit()
                return
            child = self.dir_stack.pop()
            self.load_dir(self.current_dir, select_path=child)
            return
        if action_id in [ACTION_SHOW_INFO, ACTION_CONTEXT_MENU] and self.getFocusId() == CONTROL_LIST:
            li = self.list_control.getSelectedItem()
            if li and li.getProperty("isfolder") != "true":
                self.open_detail(li)
            return
        super().onAction(action)

    def onClick(self, controlId):
        if controlId != CONTROL_LIST:
            return
        li = self.list_control.getSelectedItem()
        if not li:
            return
        path = li.getProperty("path")
        if li.getProperty("isfolder") == "true":
            self.stop_preview()
            self.dir_stack.append(path)
            self.load_dir(path)
            return
        # 给模拟器选择框 / 游戏窗口留出出现的时间
        self.hold_preview(5)
        title = li.getProperty("title")
        if not play_rom(path, title, os.path.basename(self.current_dir).lower()):
            xbmcgui.Dialog().notification(title, addon.getLocalizedString(30316), xbmcgui.NOTIFICATION_ERROR, 3000)


def show_game_browser(rom_dir, layout):
    xml_file = LAYOUT_XML.get(layout, LAYOUT_XML[1])
    log(f"Show game browser: {rom_dir} ({xml_file})")
    window = GameBrowserWindow(xml_file, addon.getAddonInfo("path"), "default", "1080i", rom_dir=rom_dir)
    window.doModal()
    del window
