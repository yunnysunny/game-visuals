import os
import xml.etree.ElementTree as ET
import urllib.parse

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

# from .mywindow import MyWindow  # 如果在同一个文件可以省略

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
            # 使用正确的 RunScript 调用方式
            addon_id = self.addon.getAddonInfo("id")
            xbmc.executebuiltin(f'RunScript({addon_id}, dir={urllib.parse.quote_plus(selected_dir)})')
            return
        # 如果没有 last_dir，显示选择器
        self.log("Routing to root directory (show selector)", level=xbmc.LOGINFO)
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

 