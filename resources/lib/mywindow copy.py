import xbmc
import xbmcgui
import xbmcplugin

from .utils import log

class MyWindow(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        self.items = kwargs.get("items", [])
        self.base_url = kwargs.get("base_url", "")
        self.handle = kwargs.get("handle", 0)
        log("MyWindow initialized")

    def onInit(self):
        # 获取列表控件
        log("MyWindow onInit")
        self.list_control = self.getControl(101)
        self.title_control = self.getControl(102)
        self.cover_control = self.getControl(103)
        self.plot_control = self.getControl(104)
        self.video_control = self.getControl(105)
        # 填充列表
        # for label, trailer in self.items:
        #     li = xbmcgui.ListItem(label)
        #     li.setProperty("trailer", trailer)
        #     self.list_control.addItem(li)
        # 填充列表
        for game in self.items:
            li = xbmcgui.ListItem(game["title"])
            li.setProperty("trailer", game.get("trailer", ""))
            li.setProperty("thumb", game.get("thumb", ""))
            li.setProperty("rom", game.get("rom", ""))
            li.setProperty("plot", game.get("plot", ""))
            self.list_control.addItem(li)

        # 默认选中第一个
        if self.list_control.size() > 0:
            self.list_control.selectItem(0)
            self.refreshPreview(0)
        log("MyWindow onInit done")
    def onFocus(self, controlId):
        if controlId == 101:
            pos = self.list_control.getSelectedPosition()
            self.refreshPreview(pos)
    def onClick(self, controlId):
        if controlId == 101:
            pos = self.list_control.getSelectedPosition()
            item = self.list_control.getListItem(pos)
            rom_path = item.getProperty("rom")
            if rom_path:
                log(f"Playing ROM via RetroPlayer: {rom_path}", xbmc.LOGINFO)
                play_title = item.getLabel()
                li = xbmcgui.ListItem(item.getLabel())
                li.setPath(rom_path)   # 明确告诉 ListItem 代表哪个文件
                li.setInfo('game', {
                    'Title': play_title
                })
                xbmc.Player().play(rom_path, li)
                xbmcplugin.endOfDirectory(self.handle, succeeded=True, cacheToDisc=False)  # ✅ 必须收尾


    def refreshPreview(self, pos):
        log("MyWindow refreshPreview")
        item = self.list_control.getListItem(pos)
        thumb = item.getProperty("thumb")
        trailer = item.getProperty("trailer")
        title = item.getLabel()
        plot = item.getProperty("plot")

        # 设置封面
        if thumb:
            self.cover_control.setImage(thumb)

        # 设置标题
        self.title_control.setLabel(title)

        # 设置简介
        self.plot_control.setText(plot)

        # 播放预览
        if trailer:
            xbmc.Player().play(trailer, windowed=True)

# if __name__ == "__main__":
#     items = [
#         ("Game 1", "special://home/media/trailer1.mp4"),
#         ("Game 2", "special://home/media/trailer2.mp4")
#     ]
#     w = MyWindow("mywindow.xml", xbmcaddon.Addon().getAddonInfo("path"), "default", "720p", items=items)
#     w.doModal()
#     del w
