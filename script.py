import sys
from urllib.parse import unquote_plus
import xbmc
import xbmcgui
import xbmcaddon
import urllib.parse as urlparse
from resources.lib.mywindow import MyWindow

# 获取 addon 信息
addon = xbmcaddon.Addon()

# sys.argv[1] 是传过来的参数
args = sys.argv[1] if len(sys.argv) > 1 else ""
params = dict(urlparse.parse_qsl(args))

if __name__ == "__main__":
    dir = unquote_plus(params.get("dir", ""))
    xbmc.log(f"[GamePoster] Script started with dir: {dir}", xbmc.LOGINFO)
    xbmc.log(f"[GamePoster] Script args: {sys.argv}", xbmc.LOGINFO)
    xbmc.log(f"[GamePoster] Script params: {params}", xbmc.LOGINFO)
    
    if not dir:
        xbmc.log("[GamePoster] No directory provided, exiting", xbmc.LOGWARNING)
        exit()
        
    w = MyWindow(
        "mywindow.xml",
        addon.getAddonInfo('path'),
        "default",
        "720p",
        dir=dir
    )
    w.doModal()
    del w
