import xbmc
# import xbmcgui
import os
import xml.etree.ElementTree as ET
import zipfile
import xbmcvfs

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
                thumb = g.findtext("thumbnail", None)
                fanart = g.findtext("image", None)
                trailer = g.findtext("video", None)
                release_date = g.findtext("releasedate", "")
                genre = g.findtext("genre", "")
                year = 0
                rating = g.findtext("rating", 0)
                if thumb:
                    thumb = os.path.normpath(os.path.join(directory, thumb))
                    if not os.path.exists(thumb):
                        thumb = None
                if fanart:
                    fanart = os.path.normpath(os.path.join(directory, fanart))
                    if not os.path.exists(fanart):
                        fanart = None
                if trailer:
                    trailer = os.path.normpath(os.path.join(directory, trailer))
                    if not os.path.exists(trailer):
                        trailer = None
                if fname.startswith("./"):
                    fname = fname[2:]  # 去掉前两个字符
                
                rom_path = os.path.normpath(os.path.join(directory, fname))
                if not os.path.exists(rom_path):
                    continue
                if release_date and len(release_date) >= 4:
                    year = int(release_date[:4])
                if rating:
                    rating = float(rating)
                game_info[fname] = {
                    "path": rom_path,
                    "title": title,
                    "plot": plot,
                    "thumb": thumb,
                    "fanart": fanart,
                    "trailer": trailer,
                    "genre": genre,
                    "year": year,
                    "rating": rating,
                }
            log(f"Found ROM list: {game_info}", level=xbmc.LOGINFO)
        except Exception as e:
            log(f"parse xml file error: {e}", level=xbmc.LOGWARNING)
            # parse_error = self.addon.getLocalizedString(30302)
            # xbmcgui.Dialog().notification(parse_error, str(e))
    return game_info

def extract_rom(zip_path, file_exts):
    """解压 zip 文件"""
    # 解压目标路径
    extract_dir = xbmcvfs.translatePath("special://temp/roms/")
    if not xbmcvfs.exists(extract_dir):
        xbmcvfs.mkdirs(extract_dir)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        file_list = zf.namelist()
        total = len(file_list)
        if total != 1:
            return None
        file = file_list[0]
        if not file.endswith(file_exts):
            return None
        zf.extract(file, extract_dir)

    return os.path.join(extract_dir, file_list[0])  # 返回第一个解压的文件路径