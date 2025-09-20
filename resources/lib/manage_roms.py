import sys
import xbmcaddon
import xbmcgui
import urllib.parse

addon = xbmcaddon.Addon()

def manage_roms():
    rom_dirs = addon.getSetting("rom_dirs").split(";") if addon.getSetting("rom_dirs") else []

    while True:
        options = rom_dirs + ["[ 添加新目录 ]", "[ 完成 ]"]
        dialog = xbmcgui.Dialog()
        choice = dialog.select("ROM 目录管理", options)

        if choice < 0:
            break
        elif choice == len(rom_dirs):
            new_dir = dialog.browse(3, "选择ROM目录", "files", "", False, False, "")
            if new_dir and new_dir not in rom_dirs:
                rom_dirs.append(new_dir)
        elif choice == len(rom_dirs) + 1:
            break
        else:
            if dialog.yesno("删除目录", f"要删除吗？\n{rom_dirs[choice]}"):
                rom_dirs.pop(choice)

    addon.setSetting("rom_dirs", ";".join(rom_dirs))

def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    action = params.get("action")

    if action == "manage_roms":
        manage_roms()

if __name__ == "__main__":
    router(sys.argv[2][1:])  # sys.argv[2] 形如 "?action=manage_roms"
