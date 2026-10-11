"""default.py 和 script.py 的实际逻辑；入口文件只负责调用，满足 kodi-addon-checker 对入口文件行数的要求"""
import urllib.parse

import xbmc


def run_plugin(argv):
    """插件入口（default.py）：argv 为 [base_url, handle, query]"""
    import xbmcaddon
    import xbmcplugin
    from .router import GameDirectoryPlugin

    # 👇 绝对要出现在日志里的测试语句（放在最前面）
    xbmc.log("[GamePoster] 插件启动！正在加载 default.py", level=xbmc.LOGINFO)

    # ===== Debug =====
    # try:
    #     import debugpy
    #     debugpy.listen(("0.0.0.0", 5678))   # 在 5678 端口等待
    #     # 只在第一次 attach 时等待客户端，避免卡住
    #     if "--debug" in argv:
    #         debugpy.wait_for_client()
    #         print("Debugger attached")
    # except Exception as e:
    #     print("debugpy not available:", e)
    # =================

    handle = int(argv[1])
    args = urllib.parse.parse_qs(argv[2][1:]) if len(argv) > 2 else {}

    # 设置支持的排序方式
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_TITLE)   # 按标题
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_DATE)    # 按日期
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_SIZE)    # 按大小
    # xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_GENRE)   # 按类别

    GameDirectoryPlugin(handle, argv[0], args, xbmcaddon.Addon()).route()


def run_script(argv):
    """脚本入口（script.py）：argv[1] 是 RunScript 传过来的参数"""
    params = dict(urllib.parse.parse_qsl(argv[1] if len(argv) > 1 else ""))
    xbmc.log(f"[GamePoster] Script params: {params}", xbmc.LOGINFO)
    rom_dir = params.get("dir", "")
    if not rom_dir:
        xbmc.log("[GamePoster] No directory provided, exiting", xbmc.LOGWARNING)
    elif params.get("action") == "detail":
        from .detail_window import show_game_detail
        show_game_detail(rom_dir, params.get("file", ""), params.get("rom_dirname", ""))
    elif params.get("action") == "platforms":
        from .platform_window import show_platform_browser
        show_platform_browser(rom_dir, int(params.get("layout", 1)))
    else:
        from .browser_window import show_game_browser
        show_game_browser(rom_dir, int(params.get("layout", 1)))
