# rom_extensions.py
"""
游戏ROM文件后缀名集合
这个文件包含了所有常见的游戏ROM文件扩展名
"""

ROM_EXTENSIONS = (
    # 常见主流平台
    ".nes",  # Nintendo Entertainment System
    ".smc", ".sfc",  # Super Nintendo
    ".n64", ".v64", ".z64",  # Nintendo 64
    ".gb",  # Game Boy
    ".gbc",  # Game Boy Color
    ".gba",  # Game Boy Advance
    ".nds",  # Nintendo DS
    ".gen", ".md",  # Sega Genesis/Mega Drive
    ".sms",  # Sega Master System
    ".gg",  # Sega Game Gear
    ".iso", ".bin", ".cue",  # CD-ROM consoles (PS1, Saturn, etc.)
    ".pce",  # PC Engine/TurboGrafx-16
    ".a26",  # Atari 2600
    
    # 其他经典/流行平台
    ".sg", ".wsc",  # WonderSwan
    ".ngp", ".ngc",  # Neo Geo Pocket/Color
    ".vb",  # Virtual Boy
    ".fds",  # Famicom Disk System
    ".smd",  # Sega Mega Drive (alternative format)
    ".32x",  # Sega 32X
    ".pkg", ".int",  # Early computer platforms
    
    # 冷门、特殊或街机平台
    ".ndd",  # Nintendo 64DD
    ".cia", ".3ds",  # Nintendo 3DS
    ".wad",  # Wii Virtual Console/WiiWare
    ".wbfs",  # Wii
    ".rvz", ".wia",  # GameCube/Wii (Dolphin compressor)
    ".chd",  # Compressed CD images (multiple platforms)
    ".m3u",  # Multi-disc playlists
    ".zip"  # Arcade ROM sets (MAME, FBNeo, etc.)
)

# 可选：提供一些辅助信息
PLATFORM_INFO = {
    ".nes": "任天堂红白机/FC",
    ".sfc": "超级任天堂/SFC",
    ".gba": "Game Boy Advance",
    ".nds": "Nintendo DS",
    ".md": "世嘉MD/Genesis",
    ".iso": "光碟游戏(PS1, Saturn等)",
    # 可以继续添加其他扩展名的说明
}

MEDIA_FOLDERS = ["images", "videos"]

def is_rom_file(filename):
    """检查文件是否是ROM文件"""
    return any(filename.lower().endswith(ext) for ext in ROM_EXTENSIONS)

def get_platform_info(extension):
    """获取扩展名对应的平台信息"""
    return PLATFORM_INFO.get(extension.lower(), "未知平台")