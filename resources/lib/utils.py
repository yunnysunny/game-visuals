import xbmc
import xbmcgui
import os
import xml.etree.ElementTree as ET
import zipfile
import xbmcvfs

from .constants import ROM_DIR_INFO, ZIPPED_ROM_DIRNAMES

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
                developer = g.findtext("developer", "")
                publisher = g.findtext("publisher", "")
                players = g.findtext("players", "")
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
                    "developer": developer,
                    "publisher": publisher,
                    "players": players,
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

def play_rom(rom_path, title, rom_dirname=None):
    """通过 RetroPlayer 启动 ROM，zip 包会先解压；ROM 无效时返回 False"""
    log(f"Playing ROM via RetroPlayer: {rom_path}", xbmc.LOGINFO)
    play_path = rom_path or ""
    if rom_dirname in ZIPPED_ROM_DIRNAMES and rom_path.endswith('.zip'):
        rom_dir_info = ROM_DIR_INFO.get(rom_dirname)
        if rom_dir_info and rom_dir_info["extensions"] and len(rom_dir_info["extensions"]) > 0:
            # 创建列表副本，避免修改原始数据
            ext_list = rom_dir_info["extensions"][:]
            ext_list.remove('.zip')
            play_path = extract_rom(rom_path, tuple(ext_list))
    if not play_path:
        return False
    li = xbmcgui.ListItem(title)
    li.setPath(rom_path)   # 明确告诉 ListItem 代表哪个文件
    li.getGameInfoTag().setTitle(title)
    xbmc.Player().play(play_path, li)
    return True