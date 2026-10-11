import os
import random
import threading
import time

import xbmc
import xbmcaddon
import xbmcgui

from .browser_window import show_game_browser
from .constants import ROM_DIR_INFO, is_rom_file, platform_category
from .utils import disc_track_files, has_rom, is_skipped_folder, log, ui_language

addon = xbmcaddon.Addon()

ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92

CONTROL_SHELF = 50
CONTROL_TABS = 60
# 焦点在同一个平台上停留多久后开始播放预览视频（秒）
PREVIEW_DELAY = 1.5

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")
VIDEO_EXTS = (".mp4", ".mkv", ".avi", ".webm", ".mov")
# 分类 id → 名称的字符串 id；"all" 之外只显示有平台的分类
CATEGORIES = [("all", 30342), ("arcade", 30343), ("console", 30344), ("handheld", 30345), ("computer", 30346)]


def list_media(directory, exts):
    try:
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(exts)]
    except OSError:
        return []


def pick_screenshot(images):
    """ES 风格的 images 目录里同时有截图、封面和标题图，优先用截图"""
    shots = [p for p in images if any(k in os.path.basename(p).lower() for k in ("-image", "screenshot", "snap"))]
    pool = shots or images
    return random.choice(pool) if pool else ""


class PlatformWindow(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom_dir = kwargs.get("rom_dir", "")
        self.layout = kwargs.get("layout", 1)
        self.platforms = []
        self.category = "all"
        self.media = {}  # 平台路径 → (截图列表, 视频列表)，焦点停留时才读取
        self.window_id = None
        self.closing = False
        self.browsing = False
        self.preview = None  # 当前由本窗口启动的预览视频路径
        self.preview_started = 0
        self.lock = threading.Lock()
        self.thread = None

    def onInit(self):
        # 从游戏列表返回时也会再次调用 onInit，此时保留列表和选中位置
        self.window_id = xbmcgui.getCurrentWindowId()
        self.shelf = self.getControl(CONTROL_SHELF)
        self.tabs = self.getControl(CONTROL_TABS)
        if not self.platforms:
            self.platforms = self.scan()
            if not self.platforms:
                xbmcgui.Dialog().notification(addon.getAddonInfo("name"), addon.getLocalizedString(30350))
                self.exit()
                return
            total = sum(p["count"] for p in self.platforms)
            self.setProperty("root", self.rom_dir)
            self.setProperty("total", addon.getLocalizedString(30341).format(len(self.platforms), f"{total:,}"))
            self.fill_tabs()
            self.fill_shelf()
        self.setFocusId(CONTROL_SHELF)
        if self.thread is None:
            self.thread = threading.Thread(target=self.preview_loop, daemon=True)
            self.thread.start()

    def scan(self):
        """列出有 ROM 的平台目录，按游戏数量从多到少排列"""
        lang = ui_language()
        default_logo = os.path.join(addon.getAddonInfo("path"), "resources", "logos", "default.png")
        platforms = []
        try:
            names = os.listdir(self.rom_dir)
        except OSError as e:
            log(f"Error reading directory {self.rom_dir}: {e}", xbmc.LOGWARNING)
            return []
        for name in names:
            path = os.path.join(self.rom_dir, name)
            if not os.path.isdir(path) or is_skipped_folder(name) or not has_rom(path):
                continue
            files = os.listdir(path)
            tracks = disc_track_files(path, files)
            count = sum(1 for f in files if is_rom_file(f) and f.lower() not in tracks)
            info = ROM_DIR_INFO.get(name.lower(), {})
            logo = os.path.join(addon.getAddonInfo("path"), "resources", "logos", f"{name.lower()}.png")
            category = platform_category(name)
            platforms.append({
                "path": path,
                "name": info.get("full_name", name),
                "count": count,
                "category": category,
                "plot": info.get("description_zh", "") if lang == "zh" else info.get("description_en", ""),
                "logo": logo if os.path.exists(logo) else default_logo,
            })
        platforms.sort(key=lambda p: (-p["count"], p["name"].lower()))
        log(f"Found {len(platforms)} platforms in {self.rom_dir}")
        return platforms

    def fill_tabs(self):
        items = []
        for cat, string_id in CATEGORIES:
            count = len(self.platforms) if cat == "all" else sum(1 for p in self.platforms if p["category"] == cat)
            if not count:
                continue
            li = xbmcgui.ListItem(label=f"{addon.getLocalizedString(string_id)}  {count}")
            li.setProperty("cat", cat)
            items.append(li)
        self.tabs.reset()
        self.tabs.addItems(items)

    def fill_shelf(self):
        names = dict(CATEGORIES)
        items = []
        for p in self.platforms:
            if self.category != "all" and p["category"] != self.category:
                continue
            li = xbmcgui.ListItem(label=p["name"])
            li.setArt({"thumb": p["logo"], "icon": p["logo"]})
            li.setProperty("path", p["path"])
            li.setProperty("countnum", str(p["count"]))
            li.setProperty("count", addon.getLocalizedString(30336).format(p["count"]))
            li.setProperty("category", addon.getLocalizedString(names[p["category"]]))
            li.setProperty("plot", p["plot"])
            cached = self.media.get(p["path"])
            if cached:
                self.apply_media(li, cached)
            items.append(li)
        self.shelf.reset()
        self.shelf.addItems(items)

    def apply_media(self, li, media):
        images, videos = media
        li.setArt({"fanart": pick_screenshot(images)})
        li.setProperty("video", "true" if videos else "")

    def load_media(self, li):
        """第一次停在某个平台上时读取它的截图和视频目录，U 盘上较慢，所以不在扫描时做"""
        path = li.getProperty("path")
        media = self.media.get(path)
        if media is None:
            images_dir = os.path.join(path, "images")
            # 有的 gamelist 把预览视频也放在 images 目录里（xxx-video.mp4）
            media = (list_media(images_dir, IMAGE_EXTS),
                     list_media(os.path.join(path, "videos"), VIDEO_EXTS) or list_media(images_dir, VIDEO_EXTS))
            self.media[path] = media
            self.apply_media(li, media)
        return media

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
        """游戏列表、弹窗、游戏或其它窗口在前台时不播放预览"""
        return (self.browsing
                or xbmcgui.getCurrentWindowId() != self.window_id
                or xbmc.getCondVisibility("System.HasModalDialog | Player.HasGame"))

    def preview_loop(self):
        """后台线程：分类栏左右移动时筛选平台；焦点停留时显示截图，并在 PREVIEW_DELAY 秒后播放随机预览视频"""
        monitor = xbmc.Monitor()
        last_path = None
        focused_since = time.time()
        while not self.closing and not monitor.waitForAbort(0.25):
            with self.lock:
                if self.closing:
                    break
                now = time.time()
                try:
                    focus = self.getFocusId()
                except RuntimeError:
                    # 窗口切换过程中可能没有任何控件有焦点
                    focus = None
                if focus == CONTROL_TABS:
                    tab = self.tabs.getSelectedItem()
                    if tab and tab.getProperty("cat") != self.category:
                        self.category = tab.getProperty("cat")
                        self.stop_preview()
                        self.fill_shelf()
                        last_path = None
                if self.is_busy():
                    focused_since = now
                    continue
                li = self.shelf.getSelectedItem()
                if not li:
                    continue
                path = li.getProperty("path")
                if path != last_path:
                    last_path = path
                    focused_since = now
                    self.stop_preview()
                    continue
                _, videos = self.load_media(li)
                if not videos or now - focused_since < PREVIEW_DELAY:
                    continue
                if self.preview:
                    # 一段视频播完后换一个随机游戏的视频接着播
                    if self.is_preview_playing() or now - self.preview_started < 3:
                        continue
                    self.preview = None
                # 用户自己在播放其它媒体时不打断
                if xbmc.Player().isPlaying():
                    continue
                self.preview = random.choice(videos)
                self.preview_started = now
                log(f"Platform preview: {self.preview}")
                xbmc.Player().play(self.preview, windowed=True)

    def open_platform(self, li):
        with self.lock:
            self.browsing = True
            self.stop_preview()
        try:
            show_game_browser(li.getProperty("path"), self.layout)
        finally:
            self.browsing = False

    def exit(self):
        with self.lock:
            self.closing = True
            self.stop_preview()
        self.close()

    def onClick(self, controlId):
        if controlId == CONTROL_TABS:
            self.setFocusId(CONTROL_SHELF)
            return
        if controlId != CONTROL_SHELF:
            return
        li = self.shelf.getSelectedItem()
        if li:
            self.open_platform(li)

    def onAction(self, action):
        if action.getId() in [ACTION_PREVIOUS_MENU, ACTION_NAV_BACK]:
            self.exit()


def show_platform_browser(rom_dir, layout):
    log(f"Show platform browser: {rom_dir}")
    window = PlatformWindow("platform_shelf.xml", addon.getAddonInfo("path"), "default", "1080i",
                            rom_dir=rom_dir, layout=layout)
    window.doModal()
    del window
