import sys
import xbmc
import urllib.parse as urlparse
from resources.lib.browser_window import show_game_browser
from resources.lib.detail_window import show_game_detail

# sys.argv[1] 是传过来的参数
args = sys.argv[1] if len(sys.argv) > 1 else ""
params = dict(urlparse.parse_qsl(args))

if __name__ == "__main__":
    xbmc.log(f"[GamePoster] Script params: {params}", xbmc.LOGINFO)
    rom_dir = params.get("dir", "")
    if not rom_dir:
        xbmc.log("[GamePoster] No directory provided, exiting", xbmc.LOGWARNING)
    elif params.get("action") == "detail":
        show_game_detail(rom_dir, params.get("file", ""), params.get("rom_dirname", ""))
    else:
        show_game_browser(rom_dir, int(params.get("layout", 1)))
