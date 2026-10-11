import xbmc
import xbmcaddon
import xbmcgui
import os
import re
import xml.etree.ElementTree as ET
import zipfile
import zlib
import xbmcvfs

from .constants import CPS3_CD_SETS, ROM_DIR_INFO, ZIPPED_ROM_DIRNAMES, SKIP_FOLDERS, is_rom_file

CARD_COLOR_COUNT = 8

def card_color(media_path, name):
    """按名称稳定地选一种卡片底色（兜底封面、卡带标签共用）"""
    return os.path.join(media_path, f"cart_label_{zlib.crc32(name.encode('utf-8')) % CARD_COLOR_COUNT}.png")

def log(msg, level=xbmc.LOGINFO):
    xbmc.log(f"[GamePoster] {msg}", level)

def ui_language():
    """界面语言的 ISO 639-1 代码。简体中文等语言 Kodi 换算不出代码（返回空串），按英文名兜底"""
    code = xbmc.getLanguage(xbmc.ISO_639_1)
    if not code and xbmc.getLanguage(xbmc.ENGLISH_NAME).startswith("Chinese"):
        return "zh"
    return code

def _read_text(path, limit=64 * 1024):
    """读取 cue/gdi 等小文本文件，兼容 UTF-8 和 GBK 编码的中文文件名"""
    with open(path, "rb") as f:
        data = f.read(limit)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("gbk", errors="ignore")

def disc_track_files(directory, names):
    """返回被 .cue/.gdi 引用的轨道文件名（小写），这些文件和镜像描述文件是同一个游戏，不单独显示"""
    tracks = set()
    for name in names:
        lower = name.lower()
        if not lower.endswith((".cue", ".gdi")):
            continue
        stem = os.path.splitext(lower)[0]
        # 兜底：读不到内容时，至少隐藏同名的 .bin
        tracks.add(stem + ".bin")
        try:
            text = _read_text(os.path.join(directory, name))
        except OSError:
            continue
        if lower.endswith(".cue"):
            refs = re.findall(r'^\s*FILE\s+"?(.+?)"?\s+\S+\s*$', text, re.M | re.I)
        else:
            refs = [q or u for q, u in re.findall(r'"([^"]+)"|(\S+\.(?:bin|raw|iso))', text, re.I)]
        tracks.update(os.path.basename(ref.replace("\\", "/")).lower() for ref in refs)
    return tracks

def is_skipped_folder(name):
    """媒体、移植游戏目录，以及 .xxx 隐藏目录（其他工具的数据目录，如 .cola）"""
    return name.startswith(".") or name.lower() in SKIP_FOLDERS

def _has_chd(directory):
    try:
        return any(f.lower().endswith(".chd") for f in os.listdir(directory))
    except OSError:
        return False

def needs_cd_image(directory, filename):
    """CPS3 需要 CD 的 ROM 包，且 MAME / FBNeo 约定的位置里没有 CHD 镜像。

    按 MAME / FBNeo 的查找规则，在 ROM 所在目录下：
    ① 先找与包同名的子目录；② 克隆包再找父包同名的子目录（与 ① 是兄弟目录，不是上级目录）。
    两处任一有 .chd 即认为 CD 已齐。例如：

        G:\\roms\\cps3\\
        ├── sfiii2.zip       父包：查 sfiii2\\ → 有 CHD，不标记
        ├── sfiii2j.zip      克隆包：查 sfiii2j\\（不存在）→ 再查 sfiii2\\ → 有 CHD，不标记
        ├── redearth.zip     父包：只查 redearth\\（不存在）→ 标记需要 CD，不会借用克隆包 warzard\\ 的 CHD
        ├── warzard.zip      克隆包：查 warzard\\ → 有 CHD，不标记
        ├── sfiii2\\
        │   └── cap-3ga000.chd
        └── warzard\\
            └── cap-wzd-5.chd
    """
    stem, ext = os.path.splitext(filename)
    if ext.lower() not in (".zip", ".7z") or stem.lower() not in CPS3_CD_SETS:
        return False
    parent = CPS3_CD_SETS[stem.lower()]
    return not any(_has_chd(os.path.join(directory, name)) for name in (stem, parent) if name)

def mark_needs_cd(title, plot):
    """在标题后加"需要 CD"，简介开头说明原因；只用于显示，启动游戏时仍用原标题"""
    addon = xbmcaddon.Addon()
    hint = addon.getLocalizedString(30352)
    label = f"{title} [{addon.getLocalizedString(30351)}]"
    return label, (f"{hint}\n\n{plot}" if plot else hint)

def has_rom(directory):
    """递归检查目录下是否有 ROM，跳过媒体等非游戏目录"""
    for _, dirnames, filenames in os.walk(directory):
        dirnames[:] = [d for d in dirnames if not is_skipped_folder(d)]
        if any(is_rom_file(f) for f in filenames):
            return True
    return False

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
    target = None
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            total = len(file_list)
            if total != 1:
                return None
            file = file_list[0]
            if not file.endswith(file_exts):
                return None
            target = os.path.join(extract_dir, file)
            zf.extract(file, extract_dir)
    except (zipfile.BadZipFile, zlib.error, OSError) as e:
        # zip 损坏（如 CRC 校验失败）时清理解压了一半的文件
        log(f"Extract ROM failed: {zip_path}: {e}", level=xbmc.LOGWARNING)
        if target and os.path.isfile(target):
            try:
                os.remove(target)
            except OSError:
                pass
        return None

    return target  # 返回解压出的文件路径

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