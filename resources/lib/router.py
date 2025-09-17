import os
# import sys
import xml.etree.ElementTree as ET
import xbmc
import xbmcgui
import xbmcplugin

class GameDirectoryPlugin:
    def __init__(self, handle, base_url, args, addon):
        self.handle = handle
        self.base_url = base_url
        self.args = args
        self.addon = addon

    def route(self):
        # 如果有指定目录，显示该目录下的游戏
        directory = self.args.get("dir", [None])[0]
        if directory:
            self.list_games_in_directory(directory)
        else:
            self.list_root()

    def list_root(self):
        # 演示：列出两个固定的游戏目录
        rom_dirs = [
            "/storage/roms/nes",
            "/storage/roms/snes"
        ]
        for d in rom_dirs:
            item = xbmcgui.ListItem(label=os.path.basename(d))
            url = f"{self.base_url}?dir={d}"
            xbmcplugin.addDirectoryItem(
                handle=self.handle, url=url, listitem=item, isFolder=True
            )
        xbmcplugin.endOfDirectory(self.handle)

    def list_games_in_directory(self, directory):
        xml_file = os.path.join(directory, "game.xml")
        game_info = {}

        if os.path.exists(xml_file):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for g in root.findall("game"):
                    fname = g.get("file")
                    title = g.findtext("title", fname)
                    plot = g.findtext("plot", "")
                    thumb = g.findtext("thumb", "")
                    if thumb and not os.path.isabs(thumb):
                        thumb = os.path.join(directory, thumb)
                    game_info[fname] = {
                        "title": title,
                        "plot": plot,
                        "thumb": thumb
                    }
            except Exception as e:
                xbmcgui.Dialog().notification("解析错误", str(e))

        # 遍历目录下的实际 ROM 文件
        for file in os.listdir(directory):
            if file.endswith((".nes", ".zip", ".sfc")):
                rom_path = os.path.join(directory, file)
                meta = game_info.get(file, {"title": file, "plot": "", "thumb": ""})

                li = xbmcgui.ListItem(label=meta["title"])
                li.setInfo("video", {"title": meta["title"], "plot": meta["plot"]})
                if meta["thumb"] and os.path.exists(meta["thumb"]):
                    li.setArt({"thumb": meta["thumb"], "poster": meta["thumb"]})

                # 直接把 ROM 文件路径交给 Kodi RetroPlayer 打开
                xbmcplugin.addDirectoryItem(
                    handle=self.handle, url=rom_path, listitem=li, isFolder=False
                )
        # ✅ 告诉 Kodi 这是“电影”类内容
        xbmcplugin.setContent(self.handle, 'movies')
        # ✅ 强制使用详细视图
        xbmc.executebuiltin('Container.SetViewMode(500)')
        xbmcplugin.endOfDirectory(self.handle)
