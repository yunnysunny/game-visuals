# Using gamelist.xml

In order for this plugin to correctly display game information, a **gamelist.xml** file must be placed inside the ROM directory of each gaming platform.
This plugin does not have an automatic scraping feature, so you need to scrape game metadata on your PC first, and then copy it to the device running Kodi.

It is recommended to use [Skraper](https://www.skraper.net/) to scrape game assets. After downloading and launching it, you’ll see the initialization panel. We recommend registering and logging into the **ScreenScraper** website to gain a higher daily scraping quota:

![](../images/login-screenscraper.png)

Click **Next**, then choose **RecalBox** as the game frontend:

![](../images/recalbox.png)

Next, select the root directory of your ROMS. This folder should contain subdirectories for each platform’s ROM files:

![](../images/select-rom-base-path.png)

After selecting the folder, click **Next**. A prompt will appear asking where to save the scraped media files:

![](../images/media-paths.png)

Once this initialization process is complete, the main interface will open. At the bottom right of the main window, you’ll find a “play” style button. Click it to start scraping:

![](../images/play-btn.png)

Since information for all platforms needs to be scraped, a confirmation dialog will pop up after clicking start, reminding you that the process may take some time. Simply click **OK** to continue:

![](../images/scraper_confirm.png)

During the scraping process, you’ll see a progress bar:

![](../images/scraper_progress.png)

When scraping is complete, a sound will play and the button in the lower right corner will change to a checkmark (√):

![](../images/finished.png)

At this point, if you open any of the scraped platform directories, you’ll see a new **gamelist.xml** file along with a **media** folder.
