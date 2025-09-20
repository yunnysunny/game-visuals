import os
import xml.etree.ElementTree as ET
import urllib.parse

import xbmc
import xbmcgui
import xbmcplugin

class GameDirectoryPlugin:
    def __init__(self, handle, base_url, args, addon):
        self.handle = handle
        self.base_url = base_url
        self.args = args
        self.addon = addon

    def log(self, msg, level=xbmc.LOGINFO):
        xbmc.log(f"[GamePoster] {msg}", level)

    def route(self):

        play_rom = self.args.get("play", [None])[0]  # ✅ 新增：检测 play 参数
        play_title = self.args.get("title", [None])[0]
        if play_rom:
            # ✅ 关键：调用 PlayMedia，让 RetroPlayer 自动接管
            # Kodi 会自动识别 .nes/.zip 等格式，并用已配置的核心播放
            self.log(f"Playing ROM via RetroPlayer: {play_rom}", xbmc.LOGINFO)
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
            self.list_games_in_directory(selected_dir)
            return
        # 如果没有 last_dir，显示选择器
        self.log("Routing to root directory (show selector)", level=xbmc.LOGINFO)
        self.list_root()

    def list_root(self):
        rom_dirs_str = self.addon.getSetting("rom_dirs")
        rom_dirs = [d.strip() for d in rom_dirs_str.split("|") if d.strip()]
        if not rom_dirs:
            xbmcgui.Dialog().ok("提示", "请先在插件设置中添加 ROM 目录")
            xbmcplugin.endOfDirectory(self.handle, succeeded=False)
            return

        for d in rom_dirs:
            li = xbmcgui.ListItem(label=d)
            url = f"{self.base_url}?dir={urllib.parse.quote_plus(d)}"
            xbmcplugin.addDirectoryItem(self.handle, url, li, isFolder=True)

        xbmcplugin.endOfDirectory(self.handle)   # ✅ 根目录必须收尾

    def list_games_in_directory(self, directory):
        xml_file = os.path.join(directory, "gamelist.xml")
        self.log(f"xml file in directory: {xml_file}", level=xbmc.LOGINFO)
        game_info = {}

        if os.path.exists(xml_file):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for g in root.findall("game"):
                    fname = g.findtext("path")
                    self.log(f"Found ROM config: {fname}", level=xbmc.LOGINFO)
                    if not fname:  # 如果没有 path 属性，跳过这条记录
                        continue
                    title = g.findtext("name", fname)
                    plot = g.findtext("desc", "")
                    thumb = g.findtext("image", "")
                    trailer = g.findtext("video", "")
                    if thumb and not os.path.isabs(thumb):
                        thumb = os.path.normpath(os.path.join(directory, thumb))
                    if trailer and not os.path.isabs(trailer):
                        trailer = os.path.normpath(os.path.join(directory, trailer))
                    if fname.startswith("./"):
                        fname = fname[2:]  # 去掉前两个字符
                    
                    game_info[fname] = {
                        "title": title,
                        "plot": plot,
                        "thumb": thumb,
                        "trailer": trailer
                    }
                self.log(f"Found ROM list: {game_info}", level=xbmc.LOGINFO)
            except Exception as e:
                self.log(f"parse xml file error: {e}", level=xbmc.LOGWARNING)
                xbmcgui.Dialog().notification("解析错误", str(e))
        else:
            # 渲染子目录
            for subdir in os.listdir(directory):
                li = xbmcgui.ListItem(label=subdir)
                url = f"{self.base_url}?dir={urllib.parse.quote_plus(os.path.join(directory, subdir))}"
                xbmcplugin.addDirectoryItem(self.handle, url, li, isFolder=True)
            xbmcplugin.endOfDirectory(self.handle)
            return
        for file in os.listdir(directory):
            if file.endswith((".nes", ".zip", ".sfc")):
                rom_path = os.path.join(directory, file)
                # self.log(f"Found ROM file: {file}", level=xbmc.LOGINFO)
                meta = game_info.get(file, {"title": file, "plot": "", "thumb": "", "trailer": ""})
                # self.log(f"Found meta file: {meta}", level=xbmc.LOGINFO)
                li = xbmcgui.ListItem(label=meta["title"])
                # 获取 Video InfoTag 对象
                info_tag = li.getVideoInfoTag()
                info_tag.setTitle(meta["title"])
                info_tag.setPlot(meta["plot"])
                info_tag.setTrailer(meta["trailer"])
                if meta["thumb"] and os.path.exists(meta["thumb"]):
                    li.setArt({
                        "thumb": meta["thumb"],
                        "poster": meta["thumb"],
                        "fanart": meta["thumb"]
                    })
                else:
                    self.log(f"No thumb found for {meta['title']} {meta['thumb']}", level=xbmc.LOGINFO)


                # ✅ 关键修改：不直接播放 ROM，而是绑定一个 “虚拟 URL” 用于点击后触发 RetroPlayer
                # 使用 plugin:// 协议构造一个“跳转指令”，避免 Kodi 尝试解码 .nes
                play_url = f"{self.base_url}?play={rom_path}&title={meta['title']}"

                xbmcplugin.addDirectoryItem(
                    handle=self.handle,
                    url=play_url,
                    listitem=li,
                    isFolder=False
                )
        xbmcplugin.setContent(self.handle, 'movies')
        # viewmode 可选枚举值：https://telaak.github.io/kodi-jsonrpc-api/types/ViewMode.html
        xbmc.executebuiltin('Container.SetViewMode("list")')
        xbmcplugin.endOfDirectory(self.handle)
