# Game Visuals User Manual

Game Visuals is a Kodi video add-on. It reads the `gamelist.xml` in your ROM folders, shows each game's cover, screenshot, description and trailer, and launches games with Kodi's built-in RetroPlayer.

The screenshots in this manual were taken on Kodi 21 for Windows with the default Estuary skin and the interface language set to English.

- [Before you start](#before-you-start)
- [Adding game folders](#adding-game-folders)
- [Add-on settings](#add-on-settings)
- [Kodi default list](#kodi-default-list)
- [Game details](#game-details)
- [Platform screen](#platform-screen)
- [Custom browse layouts](#custom-browse-layouts)
- [Adding trailers](#adding-trailers)
- [Games without artwork](#games-without-artwork)
- [Launching games and emulators](#launching-games-and-emulators)
- [CPS3 games that need a CD](#cps3-games-that-need-a-cd)
- [FAQ](#faq)

## Before you start

1. **Kodi 19 or later.** Games run in Kodi's built-in RetroPlayer.
2. **Emulator cores.** The first time you launch a game for a platform, Kodi asks you to pick and install an emulator core (`game.libretro.*`). See [Launching games and emulators](#launching-games-and-emulators).
3. **gamelist.xml.** The add-on does not scrape game information itself. Generate `gamelist.xml` together with the image and video files using a tool such as Skraper, then put them in your ROM folders. See [Using gamelist.xml](gamelist-usage.md).
4. **A game controller** (optional). See [How to Add Game Controller in Kodi](how-add-joystick.md).

## Adding game folders

From the Kodi home screen, open **Add-ons → Video add-ons → Game Visuals**. The start page lists the game folders you have added:

![Add-on start page](images/user-manual/root.jpg)

- **Add a folder:** select **Add games...** and choose a ROM folder in the file browser. You can add as many folders as you like.
- **Remove a folder:** open the context menu on the folder (`C` on a keyboard, Menu on a remote) and select **Remove**.
- **Folder structure:** you can add a single platform's ROM folder, such as `E:\games\fc\roms`, or a root folder that contains one sub-folder per platform, such as the ES-DE `ROMs` folder. Sub-folders named after a platform (`nes`, `snes`, `megadrive`, ...) are shown with the platform's full name and logo. With a custom browse layout, opening a root folder shows the [Platform screen](#platform-screen).

## Add-on settings

On Kodi's **Add-ons** screen, select Game Visuals, open the context menu and choose **Settings**.

![Add-on settings](images/user-manual/settings.jpg)

| Setting | Description |
|---|---|
| Browse layout | The screen used when you open a game folder: **Kodi default list**, **A: Classic two-column**, **B: Immersive hero**, **C: Poster wall** or **D: Retro TV**. See below. The default is Kodi default list. |
| Skip media folders | Hides these folders from the lists: artwork and BIOS folders such as `images`, `videos`, `media` and `bios`; PC port folders such as `ports` and `ports3`; hidden folders whose names start with `.`; and folders that contain no ROMs (for example an `fbneo` folder holding only emulator saves). Keep this on. |

Whether or not **Skip media folders** is on, these files are never listed as games:

- BIOS files kept next to the games, such as `neogeo.zip`, `pgm.zip`, `stvbios.zip` and the 3DO `panafz1.bin`.
- Disc track files (`.bin` and so on) referenced by a `.cue` / `.gdi`; each game is listed once, by its `.cue` / `.gdi`.

## Kodi default list

With **Browse layout** set to **Kodi default list**, game folders are shown with the views provided by your Kodi skin. Use **Options → Viewtype** in the bottom-left corner to switch between list, wall and other views.

![Kodi default list](images/user-manual/default-list.jpg)

- **Play a game:** select it and press OK.
- **Show details:** open the context menu on a game and select **Game details** to open the add-on's [Game details](#game-details) screen.

![Context menu](images/user-manual/context-menu.jpg)

> Pressing `I` (Info) in the default list opens Kodi's own information screen, not the add-on's Game details screen. Use the context menu instead.

## Game details

The details screen shows everything about one game:

![Game details](images/user-manual/detail.jpg)

- **Left:** the cover and the ROM file path.
- **Below the title:** the platform name, plus year, genre, developer, publisher, players and rating. Fields missing from `gamelist.xml` are hidden; if none are present, "No more details" is shown.
- **Middle:** the trailer area. If the game has a trailer, it plays automatically with its progress shown underneath; otherwise the screenshot is shown.
- **Right:** the game description, which scrolls automatically when it is long.
- **Buttons:**
  - **Play game:** stops the trailer and launches the game.
  - **Fullscreen trailer:** plays the trailer full screen; press Back to return. Only shown for games with a trailer.
  - **Back:** closes the screen.

For games with a trailer, playback starts as soon as the screen opens:

![Game details with a trailer playing](images/user-manual/detail-trailer.jpg)

## Platform screen

When **Browse layout** is set to one of A–D, opening a root folder that contains one sub-folder per platform shows the platform screen:

![Platform screen](images/user-manual/platform-shelf.jpg)

- **Top half:** the selected platform's logo, name, game count, category and description. Platforms with preview videos get a **Preview video** tag.
- **Preview area:** first shows a screenshot of a random game on the platform. After the platform stays selected for about 1.5 seconds, a random game's preview video plays, followed by another when it ends.
- **Categories:** press ↑ to move to the category bar, then use ← → to switch between All / Arcade / Console / Handheld / Computer. The platform cards below are filtered right away. Categories without platforms are not shown.
- **Platform cards:** sorted by number of games, most first.

| Key (keyboard / remote) | Action |
|---|---|
| ← → | Switch platform; on the category bar, switch category |
| ↑ ↓ | Move between the platform cards and the category bar |
| `Enter` / OK | Open the platform in the selected browse layout |
| `Backspace`, `Esc` / Back | Close the platform screen. Pressing Back in a game list returns here with the same platform selected |

- Platform names and logos are detected the same way as in the Kodi default list: name the folders after the EmulationStation platform folders.
- Only folders that contain ROMs are shown as platforms; artwork, BIOS, PC port and hidden folders are skipped.
- If the folder you added contains ROM files directly (for example `E:\games\fc\roms`), the platform screen is skipped and the game list opens directly.

## Custom browse layouts

When **Browse layout** is set to one of A–D, opening a game folder from the add-on's start page shows that full-screen layout. All four layouts work the same way:

| Key (keyboard / remote) | Action |
|---|---|
| Arrow keys | Select a game or folder |
| `Enter` / OK | Open a folder or play a game |
| `I` / Info, `C` / Menu | Open [Game details](#game-details) |
| `Backspace`, `Esc` / Back | Go up one folder; close the layout at the top level |

When a game with a trailer stays selected for about 1.5 seconds, its trailer plays in the layout's video area. It stops when you move to another game, open the details screen or start a game.

### A: Classic two-column

The game list is on the left. On the right are the trailer or screenshot, then the cover, title, tags and description. Good for large folders you want to scan quickly.

![Layout A](images/user-manual/layout-a.jpg)

Year, genre, developer, players and rating from `gamelist.xml` are shown as tags under the title, with the rating highlighted:

![Tags in layout A](images/user-manual/layout-a-metadata.jpg)

### B: Immersive hero

The selected game's screenshot fills the background, with a large title and description on the left, the trailer in the top-right corner and a scrolling cover carousel along the bottom. Designed for TVs.

![Layout B](images/user-manual/layout-b.jpg)

### C: Poster wall

A grid of seven covers per row; move around with the arrow keys. The info bar at the bottom shows the selected game's trailer, title and description. Works best when every game has a cover.

![Layout C](images/user-manual/layout-c.jpg)

### D: Retro TV

Trailers and screenshots play on the screen of a retro TV with scanlines, and the game list on the right is styled as cartridges.

![Layout D](images/user-manual/layout-d.jpg)

## Adding trailers

A trailer is set with the `<video>` tag of each `<game>` in `gamelist.xml`. Paths are relative to the folder containing `gamelist.xml`. These are all the tags the add-on reads:

```xml
<game>
    <path>./Donkey Kong Country (U) (V1.2) [!].zip</path>
    <name>Donkey Kong Country</name>
    <desc>Game description...</desc>
    <image>./media/images/Donkey Kong Country (U) (V1.2) [!].png</image>       <!-- screenshot, used as background -->
    <thumbnail>./media/box3d/Donkey Kong Country (U) (V1.2) [!].png</thumbnail> <!-- cover -->
    <video>./videos/Donkey Kong Country (U) (V1.2) [!].mp4</video>              <!-- trailer -->
    <releasedate>19941125T000000</releasedate>  <!-- the first 4 digits are used as the year -->
    <genre>Platform</genre>
    <developer>Rareware</developer>
    <publisher>Nintendo</publisher>
    <players>1-2</players>
    <rating>0.8</rating>                        <!-- 0 to 1, shown as 8.0 / 10 -->
</game>
```

- Any video format Kodi can play works; MP4 (H.264) is recommended.
- Put trailers in a `videos` folder inside the ROM folder. With **Skip media folders** on, that folder does not appear in the game list.
- If the file referenced by `<video>` does not exist, the game is treated as having no trailer.
- Preview videos on the [Platform screen](#platform-screen) are not read from `gamelist.xml`. A random video is picked from the platform folder: from the `videos` folder first, otherwise from the `images` folder (some scrapers put `xxx-video.mp4` files there).

## Games without artwork

If a game has neither a cover nor a screenshot in `gamelist.xml`, the add-on shows a colored card with the game's name in place of the cover. The card color is the same for that game in every layout and on the details screen. The screenshot area shows "No screenshot", or "NO SIGNAL" in the Retro TV layout.

In the layout C screenshot above, Super Mario Unlimited and 加纳战机 in the second row are shown this way.

## Launching games and emulators

The first time you launch a game for a platform, Kodi shows a dialog for choosing an emulator, listing every core that supports the file type. Cores that are already installed are marked and can be used right away; choosing one that is not installed makes Kodi download and install it first.

For FC / NES games, **Nestopia** or **FCEUmm** is recommended.

## CPS3 games that need a CD

On CPS3 arcade hardware the game program is on a CD. Regular CPS3 ROM sets (such as `warzard`, `redearth`, `sfiii`, `sfiii2`, `sfiii3`, `jojo` and `jojoba`) only contain the board BIOS and keys. Without the game's CD image (CHD), the game stops at a "NO CD-ROM DRIVE" screen whichever emulator core you choose.

The add-on adds **[Needs CD]** to the titles of these games and explains why at the start of the description:

![CPS3 games that need a CD](images/user-manual/needs-cd.jpg)

There are two ways to play them:

1. **Use the NO-CD version.** ROM sets whose names end in `n` or `ne` (such as `sfiii3n`, `jojobane` and `redeartn`) contain the game data and do not need a CD. Run them with the FinalBurn Neo core. The add-on does not mark them.
2. **Add the CD image.** Put the CHD file in a folder named after the ROM set. A clone (regional or revised version) can also use the CHD in its parent set's folder. For example, the Japanese `sfiii2j` is a clone of `sfiii2`:

   ```
   G:\roms\cps3\
   ├── sfiii2.zip
   ├── sfiii2j.zip        ← looks in sfiii2j\ first, then in the parent set's sfiii2\
   └── sfiii2\
       └── cap-3ga000.chd
   ```

   Reopen the list and the mark disappears. The add-on only checks that the folder contains a `.chd` file, not that it is the right version; with the wrong version the emulator still cannot start the game.

## FAQ

**Installing an emulator core fails**

If `kodi.log` shows a 404 error for the download, Kodi's local copy of the add-on repository index is out of date and points to an old version that has been removed from the official mirror. Go to **Add-ons → Install from repository → Kodi Add-on repository**, open the context menu on the repository, choose **Check for updates**, then install again.

**Kodi crashes after a game starts**

The emulator core is usually incompatible with the ROM. For example, the old bnes core crashes on some homebrew games. Find the problem core under the game add-ons in **Add-ons → My add-ons**, uninstall it and use a different core.

**The top of the screen shows the folder name instead of the platform name**

The platform is detected from the folder name. Name your ROM folders after the EmulationStation platform folders (for example `nes`, `snes`, `megadrive`) to get the full platform name.

**The trailer does not play**

- Check that the `<video>` path is correct and the file exists.
- Keep the game selected for more than a second.
- Check that the video plays in Kodi on its own.

**"invalid ROM" is shown after selecting a game**

The zip file is usually damaged, for example a CRC check fails while extracting it. `kodi.log` contains an `Extract ROM failed` warning naming the file. Download the ROM again.

**Some files or folders are missing from the list**

BIOS files, disc track files, PC port folders, hidden folders and folders without ROMs are skipped automatically; see [Add-on settings](#add-on-settings). Turn off **Skip media folders** to show those folders.

**Some text is blank after updating the add-on**

New interface text in the add-on is loaded only after Kodi restarts.
