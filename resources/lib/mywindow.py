import xbmc
import xbmcgui
import os
import xml.etree.ElementTree as ET

from .utils import get_game_info, log
from .constants import ROM_EXTENSIONS, MEDIA_FOLDERS
import xbmcaddon

addon = xbmcaddon.Addon()  # 默认获取当前插件
# see https://alwinesch.github.io/test-xbmc/Leia/kodi-base/d9/d2e/group__kodi__key__action__ids.html
ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92  # 也是返回键（遥控器/ESC）
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_MOUSE_MOVE = 107


class MyWindow(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        # ✅ 必须调用父类构造函数！否则 XML 不加载！
        super().__init__(*args, **kwargs)
        self.dir = kwargs.get("dir", "")
        self.dir_stack = []
        self.trailer = None
        log("MyWindow initialized")

    def onInit(self):
        # 获取列表控件
        log("MyWindow onInit")
        try:
            self.list_control = self.getControl(101)
            log(f"List control obtained: {self.list_control}")
            self.title_control = self.getControl(102)
            log(f"Title control obtained: {self.title_control}")
            self.cover_control = self.getControl(103)
            log(f"Cover control obtained: {self.cover_control}")
            self.plot_control = self.getControl(104)
            log(f"Plot control obtained: {self.plot_control}")
            # self.video_control = self.getControl(105)
        except Exception as e:
            log(f"Error getting controls: {e}")
            return
        # 填充列表
        self.refresh_list()
        # 手动设置焦点到列表控件
        try:
            self.setFocus(self.list_control)
            log("Focus set to list control")
        except Exception as e:
            log(f"Error setting focus: {e}")
        

        log("MyWindow onInit done")
    def onAction(self, action):
        # 捕获返回键（ACTION_NAV_BACK = 10）
        action_id = action.getId()
        log(f"MyWindow onAction {action_id}")
        if action_id in [ACTION_PREVIOUS_MENU, ACTION_NAV_BACK]:  # 返回键
            log("用户按下了返回键（Back/ESC）")
            if len(self.dir_stack) <= 1:
                log(f"close onAction")
                self.close()
                return  # ✅ 关键：return 不调用 super()，阻止默认关闭行为
            self.dir_stack.pop()
            last_dir = self.dir_stack[-1]
            log(f"last_dir onAction {last_dir}")
            self.dir = last_dir
            self.refresh_list(False)
            return  # ✅ 关键：return 不调用 super()，阻止默认关闭行为
        if action_id in [ACTION_MOVE_UP, ACTION_MOVE_DOWN, ACTION_MOUSE_MOVE]:
            control = self.getFocusId()
            if control == 101:
                log(f"use refreshPreview move onAction {action_id}")
                pos = self.list_control.getSelectedPosition()
                self.refreshPreview(pos)
                return
        # ✅ 其他事件交给父类处理
        log(f"use super onAction {action_id}")
        super().onAction(action)
    # def getGameInfo(self):
    #     directory = self.dir
    #     xml_file = os.path.join(directory, "gamelist.xml")
    #     log(f"xml file in directory: {xml_file}", level=xbmc.LOGINFO)
    #     game_info = {}

    #     if os.path.exists(xml_file):
    #         try:
    #             tree = ET.parse(xml_file)
    #             root = tree.getroot()
    #             for g in root.findall("game"):
    #                 fname = g.findtext("path")
    #                 log(f"Found ROM config: {fname}", level=xbmc.LOGINFO)
    #                 if not fname:  # 如果没有 path 属性，跳过这条记录
    #                     continue
    #                 title = g.findtext("name", fname)
    #                 plot = g.findtext("desc", "")
    #                 thumb = g.findtext("image", "")
    #                 trailer = g.findtext("video", "")
    #                 if thumb:
    #                     thumb = os.path.normpath(os.path.join(directory, thumb))
    #                     if not os.path.exists(thumb):
    #                         thumb = None
    #                 if trailer:
    #                     trailer = os.path.normpath(os.path.join(directory, trailer))
    #                     if not os.path.exists(trailer):
    #                         trailer = None
    #                 if fname.startswith("./"):
    #                     fname = fname[2:]  # 去掉前两个字符
                    
    #                 rom_path = os.path.normpath(os.path.join(directory, fname))
    #                 if not os.path.exists(rom_path):
    #                     continue
    #                 game_info[fname] = {
    #                     "path": rom_path,
    #                     "title": title,
    #                     "plot": plot,
    #                     "thumb": thumb,
    #                     "trailer": trailer
    #                 }
    #             log(f"Found ROM list: {game_info}", level=xbmc.LOGINFO)
    #         except Exception as e:
    #             log(f"parse xml file error: {e}", level=xbmc.LOGWARNING)
    #             parse_error = self.addon.getLocalizedString(30302)
    #             xbmcgui.Dialog().notification(parse_error, str(e))
    #     return game_info
    def refresh_list(self, record_history=True):
        """刷新当前目录内容"""
        log(f"MyWindow refresh_list called with dir: {self.dir}")
        self.list_control.reset()
        game_info = get_game_info(self.dir)
        # 修复：dir 是单个路径字符串，不需要 split
        if not self.dir:
            log("No directory provided to refresh_list")
            return
        skip_media_folders = addon.getSettingBool("skip_media_folders")
        try:
            files_list = os.listdir(self.dir)
            log(f"Found {len(files_list)} items in directory: {files_list[:5]}...")  # 只显示前5个
            
            for item in files_list:
                full_path = os.path.join(self.dir, item)
                if os.path.isdir(full_path):
                    if len(os.listdir(full_path)) == 0:
                        continue
                    if skip_media_folders and item.lower() in MEDIA_FOLDERS:
                        log(f"Skipping media folder: {item}", level=xbmc.LOGINFO)
                        continue
                if os.path.isfile(full_path) and not item.endswith(ROM_EXTENSIONS):
                    continue
                properties = game_info.get(item, {})
                thumb = properties.get("thumb", "DefaultGame.png")
                title = properties.get("title", item)

                   
                list_item = xbmcgui.ListItem(label=title)
                list_item.setProperty("path", full_path)
                list_item.setProperty("title", title)
                list_item.setProperty("trailer", properties.get("trailer", ""))
                list_item.setProperty("thumb", thumb)
                list_item.setProperty("plot", properties.get("plot", ""))
                list_item.setArt({
                    'poster': thumb,
                    'fanart': thumb,
                    'thumb': thumb,
                })
                tag = list_item.getGameInfoTag()
                tag.setTitle(title)
                list_item.setInfo('game', {'title': title})

                log(f"Adding item: {item} {properties} ${list_item.getLabel()}")
                self.list_control.addItem(list_item)
            log(f"Successfully added {len(files_list)} items to list control")
            if record_history:
                self.dir_stack.append(self.dir)
                    # 默认选中第一个
            if self.list_control.size() > 0:
                self.list_control.selectItem(0)
                self.refreshPreview(0)
        except Exception as e:
            log(f"Error reading directory {self.dir}: {e}")
    def onFocus(self, controlId):
        log(f"emit onFocus {controlId}")
        if controlId == 101:
            pos = self.list_control.getSelectedPosition()
            self.refreshPreview(pos)
        else:
            log(f"MyWindow onFocus {controlId}")
    def onClick(self, controlId):
        if controlId == 101:
            # pos = self.list_control.getSelectedPosition()
            item = self.list_control.getSelectedItem()
            selected_name = item.getLabel()
            selected_path = item.getProperty("path")

            if os.path.isdir(selected_path):
                # 进入子目录
                self.dir = selected_path
                self.refresh_list()
                return
            if selected_path:
                log(f"Playing ROM via RetroPlayer: {selected_path}", xbmc.LOGINFO)
                li = xbmcgui.ListItem(selected_name)
                li.setPath(selected_path)   # 明确告诉 ListItem 代表哪个文件
                li.setInfo('game', {
                    'title': selected_name
                })
                xbmc.Player().play(selected_path, li)


    def refreshPreview(self, pos):
        item = self.list_control.getListItem(pos)
        thumb = item.getProperty("thumb")
        trailer = item.getProperty("trailer")
        title = item.getProperty("title")
        plot = item.getProperty("plot")
        log(f"MyWindow refreshPreview {pos} {thumb} {trailer} {title} {plot}")

        # 设置封面
        if thumb:
            self.cover_control.setImage(thumb)

        # 设置标题
        self.title_control.setLabel(title)

        # 设置简介
        self.plot_control.setText(plot)

        # 播放预览
        # if trailer and trailer != self.trailer:
        #     xbmc.Player().play(trailer, windowed=True)
        #     self.trailer = trailer

