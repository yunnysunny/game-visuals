import xbmc

def log(msg, level=xbmc.LOGINFO):
    xbmc.log(f"[GamePoster] {msg}", level)