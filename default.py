# default.py
import sys
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.router import Router

# ===== Debug =====
try:
    import debugpy
    debugpy.listen(("0.0.0.0", 5678))   # 在 5678 端口等待
    # 只在第一次 attach 时等待客户端，避免卡住
    if "--debug" in sys.argv:
        debugpy.wait_for_client()
        print("Debugger attached")
except Exception as e:
    print("debugpy not available:", e)
# =================

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]
ARGS = urllib.parse.parse_qs(sys.argv[2][1:])

router = Router(HANDLE, BASE_URL, ARGS, ADDON)

if __name__ == "__main__":
    router.route()
