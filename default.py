# default.py
import sys
import urllib.parse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.router import GameDirectoryPlugin

# 👇 绝对要出现在日志里的测试语句（放在最前面）
xbmc.log("[GamePoster] 插件启动！正在加载 default.py", level=xbmc.LOGINFO)



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
ARGS = urllib.parse.parse_qs(sys.argv[2][1:]) if len(sys.argv) > 2 else {}

# 设置支持的排序方式
xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_TITLE)   # 按标题
xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_DATE)    # 按日期
xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_SIZE)    # 按大小
# xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_GENRE)   # 按类别

router = GameDirectoryPlugin(HANDLE, BASE_URL, ARGS, ADDON)

if __name__ == "__main__":
    router.route()
