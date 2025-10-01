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

ROM_DIR_INFO = {
    "amstradcpc": {
        "full_name": "Amstrad CPC",
        "platform": "amstradcpc",
        "core/emu": ["cap32"],
        "extensions": [".7z", ".cdt", ".dsk", ".m3u", ".sna", ".tap", ".voc", ".zip"],
        "description_zh": "Amstrad CPC 是1980年代英国流行的8位家用电脑，广泛用于游戏和教育。",
        "description_en": "The Amstrad CPC was a popular 8-bit home computer in the 1980s, widely used for gaming and education in the UK."
    },
    "amstradgx4000": {
        "full_name": "Amstrad GX4000",
        "platform": "amstradgx4000",
        "core/emu": ["cap32"],
        "extensions": [".cdt", ".cpr", ".dsk", ".m3u", ".sna", ".tap", ".voc", ".zip"],
        "description_zh": "Amstrad GX4000 是 Amstrad CPC 的游戏主机版本，仅在欧洲发售，拥有少量独占游戏。",
        "description_en": "The Amstrad GX4000 was the console version of the CPC, released only in Europe with a limited library of exclusive games."
    },
    "arcade": {
        "full_name": "Arcade",
        "platform": "arcade",
        "core/emu": ["mame2003_plus", "AdvanceMame", "mame2010", "mame2016", "fbalpha2012", "fbneo", "FbneoSA"],
        "extensions": [".7z", ".cmd", ".zip"],
        "description_zh": "街机游戏集合，支持经典街机主板如 Neo Geo、CPS1/2、System 16 等，使用 MAME 或 Final Burn 模拟。",
        "description_en": "Arcade game collection supporting classic arcade boards like Neo Geo, CPS1/2, System 16, emulated via MAME or Final Burn."
    },
    "mame": {
        "full_name": "Arcade MAME",
        "platform": "arcade",
        "core/emu": ["mame2003_plus", "AdvanceMame", "mame2010", "mame2016", "fbalpha2012", "fbneo", "FbneoSA"],
        "extensions": [".7z", ".cmd", ".zip"],
        "description_zh": "基于 MAME 的街机模拟器，兼容大量经典街机游戏，推荐用于高精度还原。",
        "description_en": "MAME-based arcade emulator supporting a vast library of classic arcade titles; recommended for high-accuracy emulation."
    },
    "atari2600": {
        "full_name": "Atari 2600",
        "platform": "atari2600",
        "core/emu": ["Stella", "STELLASA"],
        "extensions": [".7z", ".a26", ".bin", ".zip"],
        "description_zh": "雅达利2600是1977年推出的首款主流家用游戏机，拥有数千款经典游戏，如《太空侵略者》。",
        "description_en": "The Atari 2600, launched in 1977, was the first mainstream home video game console, featuring thousands of classics like 'Space Invaders'."
    },
    "atari5200": {
        "full_name": "Atari 5200",
        "platform": "atari5200",
        "core/emu": ["a5200", "atari800"],
        "extensions": [".7z", ".a52", ".atr", ".atx", ".bin", ".cas", ".cdm", ".rom", ".xex", ".xfd", ".zip"],
        "description_zh": "雅达利5200是1982年推出的增强版主机，支持更复杂的游戏和模拟器兼容性较好。",
        "description_en": "The Atari 5200, released in 1982, was an enhanced successor to the 2600 with better graphics and analog joysticks."
    },
    "atari7800": {
        "full_name": "Atari 7800",
        "platform": "atari7800",
        "core/emu": ["prosystem"],
        "extensions": [".7z", ".a78", ".bin", ".zip"],
        "description_zh": "雅达利7800是1986年推出的兼容2600的游戏机，拥有更强大的硬件和优秀的游戏阵容。",
        "description_en": "The Atari 7800, released in 1986, was backward compatible with the 2600 and featured improved hardware and strong game library."
    },
    "atari800": {
        "full_name": "Atari 800",
        "platform": "atari800",
        "core/emu": ["atari800"],
        "extensions": [".7z", ".a52", ".atr", ".atx", ".bin", ".cas", ".cdm", ".rom", ".xex", ".xfd", ".zip"],
        "description_zh": "雅达利800系列是8位家用电脑，支持教育、编程和游戏，与5200共享部分软件。",
        "description_en": "The Atari 800 series were 8-bit home computers supporting education, programming, and gaming, sharing software with the 5200."
    },
    "atarijaguar": {
        "full_name": "Atari Jaguar",
        "platform": "atarijaguar",
        "core/emu": ["virtualjaguar***"],
        "extensions": [".j64", ".jag", ".zip"],
        "description_zh": "雅达利Jaguar是1993年推出的64位主机，虽性能强大但软件稀少，是收藏家的珍品。",
        "description_en": "The Atari Jaguar, released in 1993, was a 64-bit console with powerful hardware but a small game library; a collector's item."
    },
    "atarilynx": {
        "full_name": "Atari Lynx",
        "platform": "atarilynx",
        "core/emu": ["handy", "mednafen_lynx"],
        "extensions": [".7z", ".lnx", ".zip"],
        "description_zh": "雅达利Lynx是1989年推出的首款彩色手持游戏机，支持背光屏幕和多人联机。",
        "description_en": "The Atari Lynx, released in 1989, was the first color handheld console with a backlit screen and multiplayer capabilities."
    },
    "atarist": {
        "full_name": "Atari ST",
        "platform": "atarist",
        "core/emu": ["hatari", "HATARISA"],
        "extensions": [".7z", ".dim", ".ipf", ".m3u", ".msa", ".st", ".stx", ".zip"],
        "description_zh": "雅达利ST系列是1980年代末的16位电脑，以图形和音乐能力著称，流行于欧洲。",
        "description_en": "The Atari ST series were 16-bit computers from the late 1980s, known for their graphics and music capabilities, popular in Europe."
    },
    "atomiswave": {
        "full_name": "Atomiswave",
        "platform": "atomiswave",
        "core/emu": ["flycast", "flycastsa", "flycast_32b"],
        "extensions": [".7z", ".bin", ".dat", ".lst", ".zip"],
        "description_zh": "世嘉2004年推出的街机主板，运行于Dreamcast架构，支持《沙罗曼蛇》《拳皇》等高质量游戏。",
        "description_en": "Sega's 2004 arcade board based on Dreamcast hardware, supporting high-quality titles like 'Metal Slug' and 'The King of Fighters'."
    },
    "wonderswan": {
        "full_name": "Bandai Wonderswan",
        "platform": "wonderswan",
        "core/emu": ["mednafen_wswan"],
        "extensions": [".7z", ".ws", ".zip"],
        "description_zh": "万代1999年推出的黑白手持机，专为日本市场设计，拥有《最终幻想》和《妖怪手表》等优秀作品。",
        "description_en": "Bandai's 1999 monochrome handheld, designed for Japan, featuring excellent titles like 'Final Fantasy' and 'Yokai Watch'."
    },
    "wonderswancolor": {
        "full_name": "Bandai Wonderswan Color",
        "platform": "wonderswancolor",
        "core/emu": ["mednafen_wswan"],
        "extensions": [".7z", ".wsc", ".zip"],
        "description_zh": "万代Wonderswan Color是1999年推出的彩色手持机，兼容黑白版，是Game Boy Color的有力竞争者。",
        "description_en": "Bandai's 1999 color handheld, backward compatible with the original Wonderswan, a strong competitor to the Game Boy Color."
    },
    "coleco": {
        "full_name": "ColecoVision",
        "platform": "colecovision",
        "core/emu": ["bluemsx", "gearcoleco"],
        "extensions": [".7z", ".bin", ".col", ".rom", ".zip"],
        "description_zh": "科莱科维森是1982年推出的高性能家用机，以出色的街机移植游戏著称，如《吃豆人》和《大金刚》。",
        "description_en": "ColecoVision, released in 1982, was a high-performance console known for its exceptional arcade ports like 'Pac-Man' and 'Donkey Kong'."
    },
    "c128": {
        "full_name": "Commodore 128",
        "platform": "c128",
        "core/emu": ["vice_x128"],
        "extensions": [".7z", ".crt", ".d64", ".g64", ".m3u", ".prg", ".t64", ".x64", ".zip"],
        "description_zh": "Commodore 128是C64的升级版，支持128KB内存和双模式运行，广泛用于教育和编程。",
        "description_en": "The Commodore 128 was an upgraded C64 with 128KB RAM and dual-mode operation, widely used for education and programming."
    },
    "c64": {
        "full_name": "Commodore 64",
        "platform": "c64",
        "core/emu": ["vice_x64", "vice_x64sc"],
        "extensions": [".7z", ".crt", ".d64", ".m3u", ".prg", ".t64", ".tap", ".zip"],
        "description_zh": "Commodore 64是历史上最畅销的单一电脑型号，拥有庞大的游戏和音乐软件库。",
        "description_en": "The Commodore 64 is the best-selling single computer model of all time, with a vast library of games and music software."
    },
    "amiga": {
        "full_name": "Commodore Amiga",
        "platform": "amiga",
        "core/emu": ["AMIBERRY*", "puae", "uae4arm_32b"],
        "extensions": [".adf", ".adz", ".dms", ".hdf", ".ipf", ".lha", ".m3u", ".uae", ".zip"],
        "description_zh": "Commodore Amiga是1985年推出的革命性多媒体电脑，擅长图形、音频和游戏，被誉为‘80年代的PC’。",
        "description_en": "The Commodore Amiga, released in 1985, was a revolutionary multimedia computer known for superior graphics, audio, and gaming."
    },
    "amigacd32": {
        "full_name": "Commodore Amiga CD 32",
        "platform": "amigacd32",
        "core/emu": ["AMIBERRY*", "puae", "uae4arm_32b"],
        "extensions": [".cue", ".hdf", ".iso", ".lha", ".zip"],
        "description_zh": "Amiga CD32是1993年推出的CD-ROM游戏主机，基于Amiga 1200，是首批消费级32位CD游戏机之一。",
        "description_en": "The Amiga CD32, released in 1993, was a CD-ROM-based game console derived from the Amiga 1200, one of the first consumer 32-bit CD gaming systems."
    },
    "c16": {
        "full_name": "Commodore Plus4",
        "platform": "c16",
        "core/emu": ["vice_xplus4"],
        "extensions": [".d64", ".g64", ".t64", ".x64", ".zip"],
        "description_zh": "Commodore Plus/4是1984年推出的低成本电脑，与C64不兼容，但拥有内置软件和彩色图形。",
        "description_en": "The Commodore Plus/4, released in 1984, was a low-cost computer incompatible with the C64 but featuring built-in software and color graphics."
    },
    "vic20": {
        "full_name": "Commodore Vic 20",
        "platform": "vic20",
        "core/emu": ["vice_xvic"],
        "extensions": [".d64", ".g64", ".t64", ".x64", ".zip"],
        "description_zh": "Commodore VIC-20是1980年推出的首款百万销量家用电脑，价格亲民，适合入门用户。",
        "description_en": "The Commodore VIC-20, released in 1980, was the first home computer to sell over a million units, known for its affordability and accessibility."
    },
    "daphne": {
        "full_name": "Daphne",
        "platform": "daphne",
        "core/emu": ["HYPSEUS", "daphne"],
        "extensions": [".daphne"],
        "description_zh": "Daphne 是一个模拟激光影碟游戏（如《龙穴历险记》）的模拟器，需要原始视频文件。",
        "description_en": "Daphne is an emulator for Laserdisc arcade games like 'Dragon's Lair', requiring original video files for playback."
    },
    "ports/doom": {
        "full_name": "Doom",
        "platform": "pc",
        "core/emu": ["chocolate-doom", "lzdoom", "prboom"],
        "extensions": [".doom", ".iwad", ".pwad", ".wad"],
        "description_zh": "Doom 是1993年发布的革命性第一人称射击游戏，支持自定义关卡和模组，是FPS的奠基之作。",
        "description_en": "Doom, released in 1993, was a revolutionary first-person shooter that pioneered modding and level design, laying the foundation for the FPS genre."
    },
    "pc": {
        "full_name": "DOS x86",
        "platform": "pc",
        "core/emu": ["dosbox_pure", "DOSBOXSDL2", "dosbox_svn"],
        "extensions": [".bat", ".com", ".exe", ".sh", ".zip", ".dosz"],
        "description_zh": "DOS游戏是1980-1990年代PC平台的经典游戏，如《仙剑奇侠传》《暗黑破坏神》，需DOSBox模拟运行。",
        "description_en": "DOS games were classics from the 1980s–1990s on PC platforms, such as 'Chinese Paladin' and 'Diablo', requiring DOSBox for emulation."
    },
    "easyrpg": {
        "full_name": "EasyRPG",
        "platform": "easyrpg",
        "core/emu": ["easyrpg"],
        "extensions": [".ldb"],
        "description_zh": "EasyRPG 是用于运行 RPG Maker 制作的RPG游戏的开源引擎，支持Windows、Linux和移动设备。",
        "description_en": "EasyRPG is an open-source engine for running RPG Maker-created RPG games, compatible with Windows, Linux, and mobile devices."
    },
    "fbneo": {
        "full_name": "Final Burn Neo",
        "platform": "arcade",
        "core/emu": ["fbneo", "fbalpha2012", "FbneoSA", "mame2003_plus"],
        "extensions": [".7z", ".zip"],
        "description_zh": "Final Burn Neo 是一个高性能街机模拟器，专注于快速运行和兼容性，支持大量Neo Geo和CPS游戏。",
        "description_en": "Final Burn Neo is a high-performance arcade emulator focused on speed and compatibility, supporting many Neo Geo and CPS titles."
    },
    "gmloader": {
        "full_name": "Gamemaker Loader",
        "platform": "gmloader",
        "core/emu": ["gmloader"],
        "extensions": [".apk", ".zip"],
        "description_zh": "用于运行GameMaker Studio制作的独立游戏，通常为Android APK或压缩包格式。",
        "description_en": "Used to run indie games made with GameMaker Studio, typically distributed as Android APKs or ZIP archives."
    },
    "freej2me": {
        "full_name": "Java Games",
        "platform": "freej2me",
        "core/emu": ["freej2me"],
        "extensions": [".jar"],
        "description_zh": "Java ME（J2ME）游戏是2000年代初手机游戏的主流，支持大量功能机游戏，如《贪吃蛇》《俄罗斯方块》。",
        "description_en": "Java ME (J2ME) games were the dominant mobile game format in the early 2000s, supporting classics like 'Snake' and 'Tetris'."
    },
    "karaoke": {
        "full_name": "Karaoke",
        "platform": "karaoke",
        "core/emu": ["pocketcdg"],
        "extensions": [".cdg"],
        "description_zh": "CD+G格式的卡拉OK游戏，支持歌词同步显示，常用于复古KTV设备模拟。",
        "description_en": "CD+G format karaoke games with synchronized lyrics display, commonly used for retro KTV machine emulation."
    },
    "odyssey": {
        "full_name": "Magnavox Odyssey 2",
        "platform": "odyssey2",
        "core/emu": ["o2em"],
        "extensions": [".7z", ".bin", ".zip"],
        "description_zh": "Magnavox Odyssey 2是1978年推出的早期家用游戏机，支持卡带和键盘输入，是现代主机的先驱。",
        "description_en": "The Magnavox Odyssey 2, released in 1978, was an early home console supporting cartridges and keyboard input, a pioneer of modern gaming."
    },
    "intellivision": {
        "full_name": "Mattel Intellivision",
        "platform": "intellivision",
        "core/emu": ["freeintv", "jzintv"],
        "extensions": [".7z", ".bin", ".int", ".rom", ".zip"],
        "description_zh": "Intellivision是1980年代与Atari 2600竞争的主机，拥有更复杂的控制和更高质量的游戏。",
        "description_en": "The Intellivision was a 1980s competitor to the Atari 2600, featuring more complex controls and higher-quality games."
    },
    "mplayer": {
        "full_name": "Media Player",
        "platform": "mplayer",
        "core/emu": ["ffplay", "mpv"],
        "extensions": [".avi", ".m3u", ".mkv", ".mp4", ".mov", ".mpg", ".sh", ".twi", ".wmv", ".ytb", ".mp3", ".wav", ".ogg", ".flac", ".pls", ".ogv", ".3g2", ".3gp", ".flv", ".ac3", ".webm", ".aiff", ".wma", ".opus", ".dts", ".hevc", ".rm", ".swf"],
        "description_zh": "多媒体播放器，支持几乎所有音视频格式，可用于播放电影、音乐、动画和自制内容。",
        "description_en": "A multimedia player supporting nearly all audio/video formats, ideal for playing movies, music, animations, and user-created content."
    },
    "megaduck": {
        "full_name": "MegaDuck",
        "platform": "megaduck",
        "core/emu": ["sameduck"],
        "extensions": [".7z", ".bin", ".zip"],
        "description_zh": "Mega Duck 是1992年推出的黑白手持机，外观类似Game Boy，但市场表现不佳，现为收藏品。",
        "description_en": "The Mega Duck, released in 1992, was a monochrome handheld resembling the Game Boy but with poor market success; now a collector's item."
    },
    "vectrex": {
        "full_name": "Milton Bradley Vectrex",
        "platform": "vectrex",
        "core/emu": ["vecx"],
        "extensions": [".7z", ".bin", ".gam", ".vec", ".zip"],
        "description_zh": "Vectrex是1982年推出的唯一使用矢量显示器的家用游戏机，图形清晰锐利，具有独特视觉风格。",
        "description_en": "The Vectrex, released in 1982, was the only home console using a vector display, offering crisp, sharp graphics with a unique aesthetic."
    },
    "msx": {
        "full_name": "MSX",
        "platform": "msx",
        "core/emu": ["bluemsx", "fmsx"],
        "extensions": [".7z", ".cas", ".dsk", ".m3u", ".mx1", ".mx2", ".rom", ".zip"],
        "description_zh": "MSX是1980年代日欧流行的标准化家用电脑，由微软参与制定，拥有丰富的游戏和教育软件。",
        "description_en": "MSX was a standardized home computer platform popular in Japan and Europe in the 1980s, co-developed by Microsoft, with rich software libraries."
    },
    "msx2": {
        "full_name": "MSX2",
        "platform": "msx2",
        "core/emu": ["bluemsx", "fmsx"],
        "extensions": [".7z", ".cas", ".dsk", ".m3u", ".mx1", ".mx2", ".rom", ".zip"],
        "description_zh": "MSX2是MSX的升级版，支持更强大的图形和声音，是日本80年代末最受欢迎的电脑之一。",
        "description_en": "MSX2 was an upgraded version of MSX with enhanced graphics and sound, one of the most popular home computers in late 1980s Japan."
    },
    "pc98": {
        "full_name": "NEC PC-9800",
        "platform": "pc98",
        "core/emu": ["np2kai", "nekop2"],
        "extensions": [".2hd", ".88d", ".98d", ".d88", ".d98", ".dup", ".fdd", ".fdi", ".hdd", ".hdi", ".hdm", ".hdn", ".nhd", ".tfd", ".thd", ".xdf", ".zip"],
        "description_zh": "NEC PC-98是日本1980-90年代最流行的个人电脑，运行大量日式RPG和视觉小说，如《美少女梦工厂》。",
        "description_en": "The NEC PC-98 was the most popular personal computer in Japan from the 1980s–90s, hosting many Japanese RPGs and visual novels like 'Girl's Garden'."
    },
    "pcengine": {
        "full_name": "NEC PC-Engine",
        "platform": "pcengine",
        "core/emu": ["mednafen_pce_fast", "mednafen_supergrafx"],
        "extensions": [".7z", ".bin", ".pce", ".zip"],
        "description_zh": "PC Engine是1987年由NEC和Hudson Soft推出的掌机/主机，以小巧设计和大量优秀游戏著称。",
        "description_en": "The PC Engine, released in 1987 by NEC and Hudson Soft, was a compact console known for its excellent game library and efficient design."
    },
    "pcenginecd": {
        "full_name": "NEC PC-Engine CD",
        "platform": "pcenginecd",
        "core/emu": ["mednafen_pce_fast", "mednafen_supergrafx"],
        "extensions": [".7z", ".bin", ".ccd", ".chd", ".cue", ".img", ".iso", ".pce", ".zip"],
        "description_zh": "PC Engine CD是PC Engine的CD扩展，支持全动态视频和高质量音频，是早期CD-ROM游戏的代表。",
        "description_en": "The PC Engine CD was a CD-ROM add-on for the PC Engine, supporting full-motion video and high-quality audio, an early pioneer of CD gaming."
    },
    "pcfx": {
        "full_name": "NEC PC-FX",
        "platform": "pcfx",
        "core/emu": ["mednafen_pcfx"],
        "extensions": [".ccd", ".chd", ".cue", ".toc", ".zip"],
        "description_zh": "PC-FX是1994年推出的日本专属主机，主打视觉小说和动画游戏，但市场失败。",
        "description_en": "The PC-FX, released in 1994, was a Japan-exclusive console focused on visual novels and animated games, but commercially unsuccessful."
    },
    "sgfx": {
        "full_name": "NEC Super Grafx",
        "platform": "supergrafx",
        "core/emu": ["mednafen_supergrafx", "mednafen_pce_fast"],
        "extensions": [".7z", ".ccd", ".chd", ".cue", ".pce", ".sgx", ".zip"],
        "description_zh": "Super Grafx是PC Engine的增强版，拥有更强的图形芯片，但仅发行了少数游戏，属于稀有机型。",
        "description_en": "The Super Grafx was an enhanced version of the PC Engine with improved graphics hardware, but only a few games were released, making it rare."
    },
    "tg16": {
        "full_name": "NEC TurboGrafx 16",
        "platform": "pcengine",
        "core/emu": ["mednafen_pce_fast", "mednafen_supergrafx"],
        "extensions": [".7z", ".bin", ".pce", ".zip"],
        "description_zh": "TurboGrafx-16是PC Engine在北美市场的名称，拥有《怒之铁拳》《魔界村》等经典游戏。",
        "description_en": "TurboGrafx-16 was the North American name for the PC Engine, featuring classics like 'Streets of Rage' and 'Castlevania'."
    },
    "tg16cd": {
        "full_name": "NEC TurboGrafx 16-CD",
        "platform": "pcenginecd",
        "core/emu": ["mednafen_pce_fast", "mednafen_supergrafx"],
        "extensions": [".7z", ".bin", ".ccd", ".chd", ".cue", ".img", ".iso", ".pce", ".zip"],
        "description_zh": "TurboGrafx-CD是北美版的PC Engine CD，支持CD-ROM游戏，是早期多媒体游戏的代表。",
        "description_en": "TurboGrafx-CD was the North American version of the PC Engine CD, supporting CD-ROM games as an early multimedia platform."
    },
    "n64": {
        "full_name": "Nintendo 64",
        "platform": "n64",
        "core/emu": ["mupen64plus_next", "glide64mk2", "mupen64plus_32b", "mupen64plus_next_alt", "parallel_n64_32b", "rice"],
        "extensions": [".7z", ".n64", ".v64", ".z64", ".zip"],
        "description_zh": "N64是任天堂1996年推出的3D主机，使用卡带，代表作有《超级马里奥64》《塞尔达传说：时之笛》。",
        "description_en": "The N64, released by Nintendo in 1996, was a 3D console using cartridges, famous for 'Super Mario 64' and 'The Legend of Zelda: Ocarina of Time'."
    },
    "nds": {
        "full_name": "Nintendo DS",
        "platform": "nds",
        "core/emu": ["drastic*"],
        "extensions": [".nds", ".zip"],
        "description_zh": "任天堂DS是2004年推出的双屏手持机，支持触控和无线联机，拥有庞大的游戏库。",
        "description_en": "The Nintendo DS, released in 2004, was a dual-screen handheld with touch and wireless features, boasting a massive game library."
    },
    "nes": {
        "full_name": "Nintendo Entertainment System",
        "platform": "nes",
        "core/emu": ["nestopia", "fceumm", "fceumm_mod", "mesen"],
        "extensions": [".7z", ".nes", ".nesm", ".unf", ".unif", ".zip"],
        "description_zh": "NES是任天堂1983年推出的主机，拯救了1983年游戏业大萧条，代表作有《超级马里奥》《魂斗罗》。",
        "description_en": "The NES, released by Nintendo in 1983, revived the video game industry after the 1983 crash, with classics like 'Super Mario Bros.' and 'Contra'."
    },
    "famicom": {
        "full_name": "Nintendo Famicom",
        "platform": "nes",
        "core/emu": ["nestopia", "fceumm", "fceumm_mod", "mesen"],
        "extensions": [".7z", ".nes", ".nesm", ".unf", ".unif", ".zip"],
        "description_zh": "Family Computer（红白机）是NES在日本的原名，拥有大量日本独占游戏和经典作品。",
        "description_en": "The Family Computer (Famicom) is the Japanese name for the NES, featuring many Japan-exclusive titles and classics."
    },
    "fds": {
        "full_name": "Nintendo Famicom Disk System",
        "platform": "fds",
        "core/emu": ["nestopia", "fceumm", "fceumm_mod", "mesen"],
        "extensions": [".7z", ".fds", ".zip"],
        "description_zh": "Famicom Disk System是红白机的磁盘扩展，可重复写入，支持《塞尔达传说》《恶魔城》等游戏。",
        "description_en": "The Famicom Disk System was a disk drive add-on for the Famicom, allowing rewritable storage and supporting games like 'Zelda' and 'Castlevania'."
    },
    "gameandwatch": {
        "full_name": "Nintendo Game and Watch",
        "platform": "gameandwatch",
        "core/emu": ["gw"],
        "extensions": [".7z", ".mgw", ".zip"],
        "description_zh": "Game & Watch是任天堂1980年推出的单屏手持设备，每台设备运行一个游戏，是现代掌机的雏形。",
        "description_en": "Game & Watch, released by Nintendo in 1980, was a single-screen handheld device with one game per unit, the precursor to modern handhelds."
    },
    "gb": {
        "full_name": "Nintendo Game Boy",
        "platform": "gb",
        "core/emu": ["gambatte", "gearboy", "mesen-s***", "mgba", "sameboy", "tgbdual", "vbam", "vba_next"],
        "extensions": [".7z", ".gb", ".zip"],
        "description_zh": "Game Boy是1989年推出的经典黑白手持机，凭借《俄罗斯方块》成为史上最畅销的掌机之一。",
        "description_en": "The Game Boy, released in 1989, was a classic monochrome handheld that became one of the best-selling consoles of all time thanks to 'Tetris'."
    },
    "gba": {
        "full_name": "Nintendo Game Boy Advance",
        "platform": "gba",
        "core/emu": ["mgba", "gpsp", "vbam", "vba_next"],
        "extensions": [".7z", ".gba", ".zip"],
        "description_zh": "GBA是2001年推出的32位掌机，拥有丰富的游戏库，是Game Boy系列的巅峰之作。",
        "description_en": "The GBA, released in 2001, was a 32-bit handheld with an extensive library, representing the peak of the Game Boy series."
    },
    "gbc": {
        "full_name": "Nintendo Game Boy Color",
        "platform": "gbc",
        "core/emu": ["gambatte", "gearboy", "mesen-s***", "mgba", "sameboy", "tgbdual", "vbam", "vba_next"],
        "extensions": [".7z", ".gb", ".gbc", ".zip"],
        "description_zh": "Game Boy Color是1998年推出的彩色升级版，兼容所有GB游戏，是过渡到GBA的重要机型。",
        "description_en": "The Game Boy Color, released in 1998, was a color upgrade backward compatible with all GB games, bridging the gap to the GBA."
    },
    "gamecube": {
        "full_name": "Nintendo GameCube",
        "platform": "gc",
        "core/emu": ["dolphin"],
        "extensions": [".ciso", ".gcm", ".gcz", ".iso", ".rvz", ".wbfs"],
        "description_zh": "GameCube是任天堂2001年推出的家用主机，以小巧设计和《塞尔达传说：风之杖》等游戏著称。",
        "description_en": "The GameCube, released by Nintendo in 2001, was known for its compact design and titles like 'The Legend of Zelda: The Wind Waker'."
    },
    "sfc": {
        "full_name": "Nintendo Super Famicom",
        "platform": "snes",
        "core/emu": ["snes9x", "mesen-s***", "snes9x2002", "snes9x2005_plus", "snes9x2010"],
        "extensions": [".7z", ".bs", ".bsx", ".dx2", ".fig", ".gd3", ".gd7", ".sfc", ".smc", ".st", ".swc", ".zip"],
        "description_zh": "Super Famicom是Snes在日本的名称，拥有《超能战士》《最终幻想VI》等经典JRPG。",
        "description_en": "The Super Famicom is the Japanese name for the SNES, featuring classics like 'Super Metroid' and 'Final Fantasy VI'."
    },
    "snes": {
        "full_name": "Nintendo Super Nintendo",
        "platform": "snes",
        "core/emu": ["snes9x", "mesen-s***", "snes9x2002", "snes9x2005_plus", "snes9x2010"],
        "extensions": [".7z", ".bs", ".bsx", ".dx2", ".fig", ".gd3", ".gd7", ".sfc", ".smc", ".st", ".swc", ".zip"],
        "description_zh": "SNES是1990年推出的16位主机，代表作包括《超级马里奥世界》《异形战机》《圣剑传说》。",
        "description_en": "The SNES, released in 1990, was a 16-bit console with classics like 'Super Mario World', 'Secret of Mana', and 'Alien Soldier'."
    },
    "virtualboy": {
        "full_name": "Nintendo Virtual Boy",
        "platform": "virtualboy",
        "core/emu": ["mednafen_vb"],
        "extensions": [".7z", ".vb", ".zip"],
        "description_zh": "Virtual Boy是1995年推出的3D立体手持设备，因健康问题和游戏匮乏而失败，现为收藏品。",
        "description_en": "The Virtual Boy, released in 1995, was a 3D stereoscopic handheld that failed due to health concerns and lack of games; now a collector's item."
    },
    "wii": {
        "full_name": "Nintendo Wii",
        "platform": "wii",
        "core/emu": ["dolphin"],
        "extensions": [".ciso", ".gcm", ".gcz", ".iso", ".rvz", ".wad", ".wbfs"],
        "description_zh": "Wii是2006年推出的体感主机，通过遥控器开创了家庭互动游戏时代，代表作有《Wii Sports》。",
        "description_en": "The Wii, released in 2006, was a motion-controlled console that pioneered family-friendly interactive gaming with 'Wii Sports'."
    },
    "openbor": {
        "full_name": "OpenBOR",
        "platform": "openbor",
        "core/emu": ["OPENBOR", "OpenBORff"],
        "extensions": [".pak"],
        "description_zh": "OpenBOR 是一个开源的2D格斗游戏引擎，支持用户自制游戏，类似《拳皇》风格。",
        "description_en": "OpenBOR is an open-source 2D fighting game engine supporting user-created games in a style similar to 'The King of Fighters'."
    },
    "3do": {
        "full_name": "Panasonic 3DO",
        "platform": "3do",
        "core/emu": ["opera"],
        "extensions": [".7z", ".bin", ".chd", ".cue", ".iso", ".zip"],
        "description_zh": "3DO是1993年推出的CD-ROM主机，由多个厂商联合开发，价格昂贵但技术先进。",
        "description_en": "The 3DO, released in 1993, was a CD-ROM console developed by multiple companies; expensive but technologically advanced."
    },
    "videopac": {
        "full_name": "Philips VideoPac",
        "platform": "videopac",
        "core/emu": ["o2em"],
        "extensions": [".bin", ".zip"],
        "description_zh": "Philips Videopac是Magnavox Odyssey 2在欧洲的名称，使用相同的硬件和游戏。",
        "description_en": "The Philips Videopac is the European name for the Magnavox Odyssey 2, using identical hardware and games."
    },
    "cdi": {
        "full_name": "Phillips CDI",
        "platform": "cdi",
        "core/emu": ["same_cdi"],
        "extensions": [".chd", ".iso"],
        "description_zh": "CD-i是飞利浦推出的多媒体互动设备，运行教育和游戏软件，部分游戏具有独特风格。",
        "description_en": "The CD-i was Philips' multimedia interactive device, running educational and gaming software, with some unique titles."
    },
    "pico-8": {
        "full_name": "PICO-8 fantasy console",
        "platform": "pico-8",
        "core/emu": ["Pico-8", "fake08"],
        "extensions": [".p8", ".png"],
        "description_zh": "PICO-8是一个虚构的8位幻想主机，用于创作和分享像素风格小游戏，社区活跃。",
        "description_en": "PICO-8 is a fictional 8-bit fantasy console for creating and sharing pixel-art mini-games, with a vibrant community."
    },
    "pokemini": {
        "full_name": "Pokemon Mini",
        "platform": "pokemini",
        "core/emu": ["pokemini"],
        "extensions": [".7z", ".min", ".zip"],
        "description_zh": "宝可梦Mini是任天堂2001年推出的迷你掌机，专为宝可梦IP设计，游戏数量极少。",
        "description_en": "The Pokemon Mini was Nintendo's 2001 mini-handheld designed exclusively for Pokemon-themed games; very limited library."
    },
    "pgm2": {
        "full_name": "PolyGame Master",
        "platform": "pgm2",
        "core/emu": ["multiemu***"],
        "extensions": [".zip"],
        "description_zh": "PolyGame Master是亚洲地区流行的街机主板，运行大量中文和东南亚格斗游戏。",
        "description_en": "PolyGame Master is a popular arcade board in Asia, running many Chinese and Southeast Asian fighting games."
    },
    "scummvm": {
        "full_name": "ScummVM",
        "platform": "pc",
        "core/emu": ["SCUMMVMSA", "scummvm"],
        "extensions": [".scummvm"],
        "description_zh": "ScummVM 是运行经典点击式冒险游戏的引擎，如《猴岛小英雄》《疯狂大楼》。",
        "description_en": "ScummVM is an engine for running classic point-and-click adventure games like 'Monkey Island' and 'Maniac Mansion'."
    },
    "sega32x": {
        "full_name": "Sega 32X",
        "platform": "sega32x",
        "core/emu": ["picodrive"],
        "extensions": [".32x", ".32X", ".7z", ".bin", ".md", ".smd", ".zip"],
        "description_zh": "32X是Genesis的扩展模块，用于增强3D性能，但因市场混乱和游戏稀少而失败。",
        "description_en": "The 32X was an add-on for the Genesis to enhance 3D performance, but failed due to market confusion and limited games."
    },
    "segacd": {
        "full_name": "Sega CD",
        "platform": "segacd",
        "core/emu": ["genesis_plus_gx", "picodrive"],
        "extensions": [".7z", ".chd", ".cue", ".m3u", ".iso", ".zip"],
        "description_zh": "Sega CD是Genesis的CD扩展，支持全动态视频和CD音轨，代表作有《音速小子CD》。",
        "description_en": "The Sega CD was a CD-ROM add-on for the Genesis, supporting FMV and CD audio, with classics like 'Sonic CD'."
    },
    "dreamcast": {
        "full_name": "Sega Dreamcast",
        "platform": "dreamcast",
        "core/emu": ["flycast", "flycastsa", "flycast_32b"],
        "extensions": [".7z", ".chd", ".cdi", ".gdi", ".m3u", ".zip"],
        "description_zh": "Dreamcast是世嘉1999年推出的最后一款主机，支持网络功能和高质量图形，拥有《莎木》《索尼克大冒险》等杰作。",
        "description_en": "The Dreamcast, released by Sega in 1999, was its last console, featuring online capabilities and high-quality graphics with masterpieces like 'Shenmue' and 'Sonic Adventure'."
    },
    "gamegear": {
        "full_name": "Sega Game Gear",
        "platform": "gamegear",
        "core/emu": ["gearsystem", "genesis_plus_gx", "picodrive"],
        "extensions": [".7z", ".bin", ".gg", ".zip"],
        "description_zh": "Game Gear是世嘉1990年推出的彩色手持机，比Game Boy更强大，但电池续航差。",
        "description_en": "The Game Gear, released by Sega in 1990, was a color handheld more powerful than the Game Boy, but with poor battery life."
    },
    "genesis": {
        "full_name": "Sega Genesis",
        "platform": "genesis",
        "core/emu": ["genesis_plus_gx", "genesis_plus_gx_wide", "picodrive"],
        "extensions": [".68k", ".7z", ".bin", ".gen", ".md", ".sg", ".sgd", ".smd", ".zip"],
        "description_zh": "Genesis是世嘉1989年推出的16位主机，在北美与SNES竞争，代表作有《刺猬索尼克》《暴走摩托》。",
        "description_en": "The Genesis, released by Sega in 1989, was a 16-bit console that competed with the SNES in North America, featuring 'Sonic the Hedgehog' and 'Mega Man X'."
    },
    "mastersystem": {
        "full_name": "Sega Master System",
        "platform": "mastersystem",
        "core/emu": ["gearsystem", "genesis_plus_gx", "picodrive"],
        "extensions": [".7z", ".bin", ".sms", ".zip"],
        "description_zh": "Master System是世嘉1985年推出的8位主机，虽然在北美失败，但在欧洲和巴西非常成功。",
        "description_en": "The Master System, released by Sega in 1985, was an 8-bit console that failed in North America but thrived in Europe and Brazil."
    },
    "megadrive": {
        "full_name": "Sega Mega Drive",
        "platform": "megadrive",
        "core/emu": ["genesis_plus_gx", "genesis_plus_gx_wide", "picodrive"],
        "extensions": [".68k", ".7z", ".bin", ".gen", ".md", ".sg", ".sgd", ".smd", ".zip"],
        "description_zh": "Mega Drive是Genesis在欧洲和日本的名称，是世嘉最成功的主机之一。",
        "description_en": "The Mega Drive is the European and Japanese name for the Genesis, one of Sega's most successful consoles."
    },
    "naomi": {
        "full_name": "Sega Naomi",
        "platform": "naomi",
        "core/emu": ["flycast", "flycastsa", "flycast_32b"],
        "extensions": [".7z", ".bin", ".dat", ".lst", ".zip"],
        "description_zh": "Naomi是世嘉1998年推出的街机主板，基于Dreamcast硬件，运行《VR战士》《铁拳》等高质量游戏。",
        "description_en": "The Naomi, released by Sega in 1998, was an arcade board based on Dreamcast hardware, running high-quality titles like 'Virtua Fighter' and 'Tekken'."
    },
    "saturn": {
        "full_name": "Sega Saturn**",
        "platform": "saturn",
        "core/emu": ["yabasanshiroSA", "yabasanshiro"],
        "extensions": [".bin", ".chd", ".cue", ".iso", ".mds", ".zip"],
        "description_zh": "Saturn是世嘉1994年推出的双CPU主机，图形复杂但开发困难，拥有大量日式RPG和格斗游戏。",
        "description_en": "The Saturn, released by Sega in 1994, was a dual-CPU console with complex graphics and difficult development, featuring many Japanese RPGs and fighters."
    },
    "sc-3000": {
        "full_name": "Sega SC-3000",
        "platform": "sc-3000",
        "core/emu": ["bluemsx"],
        "extensions": [".7z", ".bin", ".sg", ".zip"],
        "description_zh": "SC-3000是世嘉1983年推出的早期家用电脑，与MSX兼容，支持基本编程和游戏。",
        "description_en": "The SC-3000, released by Sega in 1983, was an early home computer compatible with MSX, supporting basic programming and games."
    },
    "sg-1000": {
        "full_name": "Sega SG-1000",
        "platform": "sg-1000",
        "core/emu": ["gearsystem", "genesis_plus_gx", "picodrive"],
        "extensions": [".7z", ".bin", ".sg", ".zip"],
        "description_zh": "SG-1000是世嘉1983年推出的首款家用游戏机，是Genesis的前身，游戏数量有限。",
        "description_en": "The SG-1000, released by Sega in 1983, was Sega's first home console and the precursor to the Genesis, with a limited game library."
    },
    "x1": {
        "full_name": "Sharp X1",
        "platform": "x1",
        "core/emu": ["x1"],
        "extensions": [".2d", ".2hd", ".7z", ".88d", ".cmd", ".d88", ".dup", ".dx1", ".hdm", ".tap", ".tfd", ".xdf", ".zip"],
        "description_zh": "Sharp X1是夏普1982年推出的日本8位电脑，支持彩色图形和声音，主要用于游戏和编程。",
        "description_en": "The Sharp X1, released by Sharp in 1982, was an 8-bit Japanese computer with color graphics and sound, primarily used for games and programming."
    },
    "x68000": {
        "full_name": "Sharp X68000",
        "platform": "x68000",
        "core/emu": ["px68k"],
        "extensions": [".2hd", ".7z", ".88d", ".cmd", ".d88", ".dim", ".dup", ".hdf", ".hdm", ".img", ".m3u", ".xdf", ".zip"],
        "description_zh": "X68000是夏普1987年推出的16/32位高性能电脑，是日本90年代街机游戏的开发平台，图形能力极强。",
        "description_en": "The X68000, released by Sharp in 1987, was a high-performance 16/32-bit computer and the primary development platform for Japanese arcade games in the 1990s."
    },
    "zxspectrum": {
        "full_name": "Sinclair ZX Spectrum",
        "platform": "zxspectrum",
        "core/emu": ["fuse"],
        "extensions": [".7z", ".rzx", ".scl", ".tap", ".trd", ".tzx", ".z80", ".zip"],
        "description_zh": "ZX Spectrum是英国1982年推出的经典8位电脑，是欧洲游戏开发的摇篮，拥有海量独立游戏。",
        "description_en": "The ZX Spectrum, released in the UK in 1982, was a classic 8-bit computer and the birthplace of European game development with a vast indie library."
    },
    "zx81": {
        "full_name": "Sinclair ZX81",
        "platform": "zx81",
        "core/emu": ["81"],
        "extensions": [".7z", ".p", ".tzx", ".zip"],
        "description_zh": "ZX81是1981年推出的廉价8位电脑，是许多英国人接触编程的起点。",
        "description_en": "The ZX81, released in 1981, was an ultra-low-cost 8-bit computer and the entry point to programming for many Britons."
    },
    "neogeo": {
        "full_name": "SNK Neo-Geo",
        "platform": "neogeo",
        "core/emu": ["fbneo", "fbalpha2012", "mame2003_plus"],
        "extensions": [".7z", ".zip"],
        "description_zh": "Neo Geo是SNK1990年推出的街机/家用一体主机，拥有顶级画质和《拳皇》《合金弹头》等经典游戏。",
        "description_en": "The Neo Geo, released by SNK in 1990, was an arcade/home一体 system with top-tier graphics and classics like 'The King of Fighters' and 'Metal Slug'."
    },
    "neocd": {
        "full_name": "SNK Neo-Geo CD",
        "platform": "neogeocd",
        "core/emu": ["neocd", "fbneo"],
        "extensions": [".7z", ".chd", ".cue", ".iso", ".zip"],
        "description_zh": "Neo Geo CD是Neo Geo的CD版本，价格更低，但加载时间长，支持大量CD-ROM游戏。",
        "description_en": "The Neo Geo CD was the CD-based version of Neo Geo, cheaper but with long load times, supporting many CD-ROM titles."
    },
    "ngp": {
        "full_name": "SNK Neo-Geo Pocket",
        "platform": "ngp",
        "core/emu": ["mednafen_ngp"],
        "extensions": [".7z", ".ngp", ".zip"],
        "description_zh": "Neo Geo Pocket是SNK1998年推出的黑白手持机，主打《拳皇》《合金弹头》掌机版。",
        "description_en": "The Neo Geo Pocket, released by SNK in 1998, was a monochrome handheld focused on ports of 'The King of Fighters' and 'Metal Slug'."
    },
    "ngpc": {
        "full_name": "SNK Neo-Geo Pocket Color",
        "platform": "ngpc",
        "core/emu": ["mednafen_ngp"],
        "extensions": [".7z", ".ngpc", ".zip"],
        "description_zh": "Neo Geo Pocket Color是1999年推出的彩色版，兼容黑白版，是Game Boy Color的有力竞争者。",
        "description_en": "The Neo Geo Pocket Color, released in 1999, was a color upgrade backward compatible with the original, a strong competitor to the Game Boy Color."
    },
    "solarus": {
        "full_name": "Solarus",
        "platform": "solarus",
        "core/emu": ["solarus"],
        "extensions": [".solarus"],
        "description_zh": "Solarus 是一个开源的《塞尔达传说》风格2D冒险游戏引擎，支持用户自制地图和剧情。",
        "description_en": "Solarus is an open-source 2D adventure game engine inspired by 'The Legend of Zelda', supporting user-created maps and stories."
    },
    "psx": {
        "full_name": "Sony Playstation",
        "platform": "psx",
        "core/emu": ["pcsx_rearmed_32b", "duckstation", "pcsx_rearmed", "swanstation"],
        "extensions": [".7z", ".bin", ".cbn", ".ccd", ".chd", ".cue", ".img", ".m3u", ".mdf", ".pbp", ".toc", ".zip"],
        "description_zh": "PlayStation是索尼1994年推出的32位主机，彻底改变了游戏行业，拥有《最终幻想VII》《合金装备》等里程碑作品。",
        "description_en": "The PlayStation, released by Sony in 1994, was a 32-bit console that revolutionized gaming with landmark titles like 'Final Fantasy VII' and 'Metal Gear Solid'."
    },
    "psp": {
        "full_name": "Sony Playstation Portable",
        "platform": "psp",
        "core/emu": ["PPSSPPSDL*", "Ppsspp"],
        "extensions": [".cso", ".iso", ".pbp"],
        "description_zh": "PSP是索尼2004年推出的掌机，支持高清画面和多媒体功能，拥有《战神》《合金装备：和平行者》等高质量游戏。",
        "description_en": "The PSP, released by Sony in 2004, was a handheld with HD graphics and multimedia features, featuring high-quality titles like 'God of War' and 'Metal Gear Solid: Peace Walker'."
    },
    "pspminis": {
        "full_name": "Sony Playstation Portable Minis",
        "platform": "psp",
        "core/emu": ["PPSSPPSDL*", "Ppsspp"],
        "extensions": [".cso", ".iso", ".pbp"],
        "description_zh": "PSP Minis是索尼为PSP推出的轻量级游戏，通常为简化版经典游戏或独立作品。",
        "description_en": "PSP Minis were lightweight games released by Sony for the PSP, often simplified versions of classics or indie titles."
    },
    "supervision": {
        "full_name": "Supervision",
        "platform": "supervision",
        "core/emu": ["potator"],
        "extensions": [".7z", ".bin", ".sv", ".zip"],
        "description_zh": "Supervision是1990年代法国推出的彩色手持机，支持触控和SD卡扩展，游戏数量稀少。",
        "description_en": "The Supervision was a color handheld released in the 1990s in France, featuring touch controls and SD card expansion; very limited library."
    },
    "tic-80": {
        "full_name": "TIC-80",
        "platform": "tic-80",
        "core/emu": ["tic80"],
        "extensions": [".tic"],
        "description_zh": "TIC-80 是一个8位幻想游戏机，用于创作和分享微型游戏，支持Lua脚本和像素艺术。",
        "description_en": "TIC-80 is an 8-bit fantasy console for creating and sharing tiny games, supporting Lua scripting and pixel art."
    },
    "uzebox": {
        "full_name": "uzebox",
        "platform": "uzebox",
        "core/emu": ["uzem"],
        "extensions": [".hex", ".uze"],
        "description_zh": "Uzebox 是一个开源的8位家用游戏机硬件平台，支持自定义固件和游戏开发。",
        "description_en": "The Uzebox is an open-source 8-bit home console hardware platform supporting custom firmware and game development."
    },
    "ports/ecwolf/games": {
        "full_name": "Wolfenstein 3D",
        "platform": "pc",
        "core/emu": ["ecwolf"],
        "extensions": [".ecwolf", ".n3d", ".sd2", ".sd3", ".sod", ".wl6"],
        "description_zh": "德军总部3D是1992年发布的经典第一人称射击游戏，是Doom的前身，使用Wolfenstein引擎。",
        "description_en": "Wolfenstein 3D, released in 1992, was a classic FPS and the precursor to Doom, using the Wolfenstein engine."
    }
}

MEDIA_FOLDERS = [
    "images", "videos", "bezels", "BGM", "bios", "bios3", "ports_scripts", "savestates", "splash",
    "downloads", "screenshots", "media"
]

def is_rom_file(filename):
    """检查文件是否是ROM文件"""
    return any(filename.lower().endswith(ext) for ext in ROM_EXTENSIONS)
