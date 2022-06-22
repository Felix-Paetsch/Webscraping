# Scrape Discord

This script allows you to scrape data from discord with Python. <br />
Currently it is able to grab all (img/video/text-)file-links from server channels or private conversations.

Last tested 20.06.22.

## Requirements
- bs4 (`pip install bs4`)
- Selenium

### You just want to get done:
Install Selenium with `pip install selenium` and put the latests [Chromedriver](https://chromedriver.chromium.org/downloads)  under the name `chromedriver.exe` in this directory.

### A little bit more to Selenium:

If you haven't uses Selenium before:
[Selenium](https://selenium-python.readthedocs.io/) is a tool that programatically interacts with a browser as if it was a real user. It is mainly used for website-testing, web-automation & web-scraping.

The script expects you to put the latest [Chromedriver](https://chromedriver.chromium.org/downloads) into this directory with the name "chromedriver.exe". You will probably also have to have Chrome itself installed.

Note that there are also ways to use Selenium with [other browsers](https://selenium-python.readthedocs.io/installation.html#drivers) and this code is easily adaptable.

## Usage
##### 1. [Update config.json](#Config)
##### 2. Open commandline in this directory
##### 3. Start the program
`python main.py` <br />
A browser-instance will open. 
##### 4. Log into Discord
##### 5. Navigate to the channel you want to scrape from
##### 6. Press \[ENTER\] (or any key)

##### Hints:
- With really long channels and long durations of scraping, sometimes it is to much data for the browser and it crashes. (For me maybe every 12 hours of scraping.) When this happened but you want to continue scraping higher up you can search for messages at the top-right with the magnifying glass. Conveniently it allows you to also sort by date so you can skip back to the time where your browser crashed. Be carefull to update the file_prefix in [config.json](#Config), since the counting will start back at 0.
- This tool can be used both on channels in discord servers and with private messages.
- During the scraping you can - although not recommended - change the currently scraped channel and the messages will just be appended to the old ones. If you have a bad timing though the program will crash. (Because it's trying to read out the messages while the new channel is loading.)

## Output
For an example output see ./out/scraped_channel_xyz_0.json. The messages will be parsed and periodically written into such files. Note that the index always starts at 0, so make sure to [update the prefix](#Config) between two scrapping sessions.
This program only saves file-links of files hosted on discord. To save space the first part of the URL is not saved. To retrieve the URL from the array entries add `https://cdn.discordapp.com/attachments/` infront of them:

`828649725355098194/937012853179822120/egq235i14le81.png`

becomes

`https://cdn.discordapp.com/attachments/828649725355098194/937012853179822120/egq235i14le81.png`

(Btw. these images are from a memes discord of a uni I went to in germany.)

## Brief explanation
Because it is somewhat important to select the best settings here is a brief explanation of what the script does:

In each *cycle* it finds the scroll-bar and presses n times at it's top to cause it to scroll up. After k cycles it goes through all messages, which are currently loaded, parses them and whites them to an output file.

(Messages do get unloaded after some time. There will be lots of duplicats. Since this programm currently only works for scraping img/video filesit is easy to filter for unique links once the scraping is done. Even though this still is a todo!)

## Config
Before running this program you will probably want to update the config.json file. Here is what each different parameter does:

- `max_images_displayed`: Fetching each and every image can be hard on your internet and slow down scraping or may cause your browser window to crash earlier due to being overloaded. This parameter sets how many images in total are loaded. You want to set it to something like 30 to be able to do captchas and navigate to you desired channels to scrape from. Set to -1 to disable/load every image.
- `init_scroll`: How many times to press the scroll-bar before we start scraping. E.g. when something recent happened which you don't care about. This does not garantee though that these messages which you don't care about will have been unloaded already. Note that you ofc can also set manually from where you start scrolling.
- `scroll_pause`: How long (in seconds, fractions allowed) to wait between cycles. Together with `cycle_stop_after` you want to set this to a value that your internet can keep up with fetching new messages.
- `cycle_stop_after`: How many times you want to press on the scrollbar for each [cycle](#brief-explanation). Setting this to low will lead to more duplicats. Setting it to high emposes the risk of messages loading in and after some amount of cycles loading out before they haved been saved once (so being skipped).
- `cycle_save_amt`: Every `cycle_save_amt` cycles all messages from these cycles are saved in an output file. Lower value means more files, but if you stop the program / something crashes more progress will be saved. 
- `cycle_amt`: After how many cycles to stop scraping. Set to -1 to only stop manually.
- `save_dir`: Where to save the files.
- `prefix`: File prefix. You probably want to change this every time you scrape. Otherwise files will get overwritton.
- `valid_file_extensions`: What type of files to look for. 

## To-Do
[ ] scrape text-messages with user-data aswell<br />
[ ] remove duplicats