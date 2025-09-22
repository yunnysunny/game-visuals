import xbmc
import xbmcgui
import os
import xml.etree.ElementTree as ET

def log(msg, level=xbmc.LOGINFO):
    xbmc.log(f"[GamePoster] {msg}", level)

def get_game_info(directory):
    xml_file = os.path.join(directory, "gamelist.xml")
    log(f"xml file in directory: {xml_file}", level=xbmc.LOGINFO)
    game_info = {}

    if os.path.exists(xml_file):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for g in root.findall("game"):
                fname = g.findtext("path")
                log(f"Found ROM config: {fname}", level=xbmc.LOGINFO)
                if not fname:  # 如果没有 path 属性，跳过这条记录
                    continue
                title = g.findtext("name", fname)
                plot = g.findtext("desc", "")
                thumb = g.findtext("image", "")
                trailer = g.findtext("video", "")
                if thumb:
                    thumb = os.path.normpath(os.path.join(directory, thumb))
                    if not os.path.exists(thumb):
                        thumb = None
                if trailer:
                    trailer = os.path.normpath(os.path.join(directory, trailer))
                    if not os.path.exists(trailer):
                        trailer = None
                if fname.startswith("./"):
                    fname = fname[2:]  # 去掉前两个字符
                
                rom_path = os.path.normpath(os.path.join(directory, fname))
                if not os.path.exists(rom_path):
                    continue
                game_info[fname] = {
                    "path": rom_path,
                    "title": title,
                    "plot": plot,
                    "thumb": thumb,
                    "trailer": trailer
                }
            log(f"Found ROM list: {game_info}", level=xbmc.LOGINFO)
        except Exception as e:
            log(f"parse xml file error: {e}", level=xbmc.LOGWARNING)
            parse_error = self.addon.getLocalizedString(30302)
            xbmcgui.Dialog().notification(parse_error, str(e))
    return game_info    