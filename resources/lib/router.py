import os
import urllib.parse

from .utils import get_game_info, log
from .constants import ROM_EXTENSIONS, MEDIA_FOLDERS
import xbmc
import xbmcgui
import xbmcplugin

VIEW_MODE_LIST = 50
VIEW_MODE_POSTER = 51
VIEW_MODE_ICON_WALL = 52
VIEW_MODE_SHIFT = 53
VIEW_MODE_INFO_WALL = 54
VIEW_MODE_WIDE_LIST = 55
VIEW_MODE_WALL = 500
VIEW_MODE_BANNER = 501
VIEW_MODE_FANART = 502
VIEW_MODE_NOW_PLAYING = 503
VIEW_MODE_MEDIA_LIST = 504

class GameDirectoryPlugin:
    def __init__(self, handle, base_url, args, addon):
        self.handle = handle
        self.base_url = base_url
        self.args = args
        self.addon = addon

    def route(self):

        play_rom = self.args.get("play", [None])[0]  # ✅ 新增：检测 play 参数
        play_title = self.args.get("title", [None])[0]
        if play_rom:
            # ✅ 关键：调用 PlayMedia，让 RetroPlayer 自动接管
            # Kodi 会自动识别 .nes/.zip 等格式，并用已配置的核心播放
            log(f"Playing ROM via RetroPlayer: {play_rom}", xbmc.LOGINFO)
            # xbmc.executebuiltin(f'PlayMedia("{play_rom}")')
            li = xbmcgui.ListItem(play_title)
            li.setPath(play_rom)   # 明确告诉 ListItem 代表哪个文件
            li.setInfo('game', {
                'Title': play_title
            })
            xbmc.Player().play(play_rom, li)
            xbmcplugin.endOfDirectory(self.handle, succeeded=True, cacheToDisc=False)  # ✅ 必须收尾

            return  # 终止后续流程，不再渲染列表
        # 2. 打开指定目录
        selected_dir = self.args.get("dir", [None])[0]
        if selected_dir:
            use_two_column = self.addon.getSettingBool("use_two_column_view")
            if use_two_column:
                # 使用正确的 RunScript 调用方式
                addon_id = self.addon.getAddonInfo("id")
                xbmc.executebuiltin(f'RunScript({addon_id}, dir={urllib.parse.quote_plus(selected_dir)})')
            else:
                self.list_games_in_directory(selected_dir)
            return
        # 如果没有 last_dir，显示选择器
        log("Routing to root directory (show selector)", level=xbmc.LOGINFO)
        self.list_root()

    def list_root(self):
        rom_dirs_str = self.addon.getSetting("rom_dirs")
        rom_dirs = [d.strip() for d in rom_dirs_str.split("|") if d.strip()]
        if not rom_dirs:
            tip = self.addon.getLocalizedString(30300)
            tip_msg = self.addon.getLocalizedString(30301)
            xbmcgui.Dialog().ok(tip, tip_msg)
            xbmcplugin.endOfDirectory(self.handle, succeeded=False)
            return

        for d in rom_dirs:
            li = xbmcgui.ListItem(label=d)
            url = f"{self.base_url}?dir={urllib.parse.quote_plus(d)}"
            xbmcplugin.addDirectoryItem(self.handle, url, li, isFolder=True)

        xbmcplugin.endOfDirectory(self.handle)   # ✅ 根目录必须收尾
    
    def list_games_in_directory(self, directory):
        game_info = get_game_info(directory)
        skip_media_folders = self.addon.getSettingBool("skip_media_folders")

        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            # log(f"Found file: {file}", level=xbmc.LOGINFO)
            if os.path.isdir(full_path):
                if len(os.listdir(full_path)) == 0:
                    continue
                if skip_media_folders and file.lower() in MEDIA_FOLDERS:
                    log(f"Skipping media folder: {file}", level=xbmc.LOGINFO)
                    continue
                li = xbmcgui.ListItem(label=file)
                url = f"{self.base_url}?dir={urllib.parse.quote_plus(full_path)}"
                xbmcplugin.addDirectoryItem(self.handle, url, li, isFolder=True)
                continue
            if os.path.isfile(full_path):
                if not file.lower().endswith(ROM_EXTENSIONS):
                    continue
                
                meta = game_info.get(file, {
                    "title": file,
                    "plot": "",
                    "thumb": "DefaultGame.png",
                    "trailer": ""
                })
                # log(f"Found meta file: {meta}", level=xbmc.LOGINFO)
                li = xbmcgui.ListItem(label=meta["title"])
                # 获取 Video InfoTag 对象
                info_tag = li.getVideoInfoTag()
                info_tag.setTitle(meta["title"])
                info_tag.setPlot(meta["plot"])
                if meta["trailer"] and os.path.exists(meta["trailer"]):
                    li.setProperty("IsPlayable", "true")
                    info_tag.setTrailer(meta["trailer"])
                #     log(f"--- Trailer found for {meta['title']} {meta['trailer']} ---", level=xbmc.LOGINFO)
                # else:
                #     log(f"No trailer found for {meta['title']} {meta['trailer']}", level=xbmc.LOGINFO)
                if meta["thumb"] and os.path.exists(meta["thumb"]):
                    li.setArt({
                        "thumb": meta["thumb"],
                        "poster": meta["thumb"],
                        "fanart": meta["thumb"]
                    })
                # else:
                #     log(f"No thumb found for {meta['title']} {meta['thumb']}", level=xbmc.LOGINFO)


                # ✅ 关键修改：不直接播放 ROM，而是绑定一个 “虚拟 URL” 用于点击后触发 RetroPlayer
                # 使用 plugin:// 协议构造一个“跳转指令”，避免 Kodi 尝试解码 .nes
                play_url = f"{self.base_url}?play={full_path}&title={meta['title']}"
                log(f"Adding playable item: {file}", level=xbmc.LOGINFO)
                xbmcplugin.addDirectoryItem(
                    handle=self.handle,
                    url=play_url,
                    listitem=li,
                    isFolder=False
                )
        xbmcplugin.setContent(self.handle, 'movies')
        # viewmode 可选枚举值：https://telaak.github.io/kodi-jsonrpc-api/types/ViewMode.html
        # https://kodi.wiki/view/HOW-TO%3AEstuary_Modification
        xbmc.executebuiltin('Container.SetViewMode(%d)' % VIEW_MODE_SHIFT)
        xbmcplugin.endOfDirectory(self.handle)

 