import os

import xbmc
import xbmcaddon
import xbmcgui

from .utils import get_game_info, log, play_rom
from .constants import ROM_DIR_INFO

addon = xbmcaddon.Addon()

ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92

CONTROL_PLAY = 10
CONTROL_TRAILER = 11
CONTROL_BACK = 12


def format_rating(rating):
    """gamelist.xml 中的评分是 0~1 的小数，转成十分制显示"""
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        return ""
    if rating <= 0:
        return ""
    if rating <= 1:
        rating *= 10
    return f"{rating:.1f} / 10"


class GameDetailWindow(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom_dir = kwargs.get("rom_dir", "")
        self.rom_file = kwargs.get("rom_file", "")
        self.rom_dirname = kwargs.get("rom_dirname", "")
        self.rom_path = os.path.join(self.rom_dir, self.rom_file)
        self.meta = get_game_info(self.rom_dir).get(self.rom_file, {})
        self.title = self.meta.get("title") or os.path.splitext(self.rom_file)[0]
        self.trailer = self.meta.get("trailer") or ""
        self.play_requested = False

    def onInit(self):
        meta = self.meta
        default_fanart = addon.getAddonInfo("fanart")
        default_logo = os.path.join(addon.getAddonInfo("path"), "resources", "logos", "default.png")
        platform = ROM_DIR_INFO.get(self.rom_dirname or os.path.basename(self.rom_dir).lower(), {})

        self.setProperty("title", self.title)
        self.setProperty("platform", platform.get("full_name", ""))
        self.setProperty("path", self.rom_path)
        self.setProperty("plot", meta.get("plot", ""))
        self.setProperty("thumb", meta.get("thumb") or meta.get("fanart") or default_logo)
        self.setProperty("fanart", meta.get("fanart") or default_fanart)
        self.setProperty("year", str(meta["year"]) if meta.get("year") else "")
        self.setProperty("genre", meta.get("genre", ""))
        self.setProperty("developer", meta.get("developer", ""))
        self.setProperty("publisher", meta.get("publisher", ""))
        self.setProperty("players", meta.get("players", ""))
        self.setProperty("rating", format_rating(meta.get("rating")))
        self.setProperty("trailer", self.trailer)

        if self.trailer:
            xbmc.Player().play(self.trailer, windowed=True)
        self.setFocusId(CONTROL_PLAY)

    def is_trailer_playing(self):
        player = xbmc.Player()
        if not self.trailer or not player.isPlayingVideo():
            return False
        return os.path.normcase(player.getPlayingFile()) == os.path.normcase(self.trailer)

    def stop_trailer(self):
        if not self.is_trailer_playing():
            return
        player = xbmc.Player()
        player.stop()
        # 等待播放器真正停止，否则紧接着启动 RetroPlayer 可能失败
        for _ in range(20):
            if not player.isPlaying():
                break
            xbmc.sleep(100)

    def exit(self):
        self.stop_trailer()
        self.close()

    def onAction(self, action):
        if action.getId() in [ACTION_PREVIOUS_MENU, ACTION_NAV_BACK]:
            self.exit()
            return
        super().onAction(action)

    def onClick(self, controlId):
        if controlId == CONTROL_PLAY:
            self.play_requested = True
            self.exit()
        elif controlId == CONTROL_TRAILER:
            if self.is_trailer_playing():
                xbmc.executebuiltin("ActivateWindow(fullscreenvideo)")
            elif self.trailer:
                xbmc.Player().play(self.trailer)
        elif controlId == CONTROL_BACK:
            self.exit()


def show_game_detail(rom_dir, rom_file, rom_dirname=""):
    """打开游戏详情页；用户点击“开始游戏”时在窗口关闭后启动 ROM"""
    log(f"Show game detail: {rom_dir} {rom_file}")
    window = GameDetailWindow(
        "game_detail.xml",
        addon.getAddonInfo("path"),
        "default",
        "1080i",
        rom_dir=rom_dir,
        rom_file=rom_file,
        rom_dirname=rom_dirname,
    )
    window.doModal()
    play_requested = window.play_requested
    title = window.title
    rom_path = window.rom_path
    del window
    if play_requested and not play_rom(rom_path, title, rom_dirname):
        xbmcgui.Dialog().notification(title, addon.getLocalizedString(30316), xbmcgui.NOTIFICATION_ERROR, 3000)
