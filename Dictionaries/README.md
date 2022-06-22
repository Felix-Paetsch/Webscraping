This directory contains scripts to scrape data from different language- and translation-oriented websites such as Langenscheidt (a german dictionary-provider) and DeepL.

# DeepL [(https://www.deepl.com/translator)](https://www.deepl.com/translator)

## Requirements
- bs4 (`pip install bs4`)
- Selenium

(See [here](https://github.com/Felix-Paetsch/Webscraping/tree/main/Discord#requirements) for more details (same requirements))

## Usage
There are two main functions:
- `set_languages(driver, source_lan, target_lan)` - Call this function (for every new language combination) to go to the according DeepL-page. `source_lan` and `target_lan` both have to be language abbreviations (e.g. "en", "nl", "de", "it") from languages supported by DeepL.
- `get_data_for_word(driver, text, wait_time)` - Call this funtion to get the translation for a given word or phrase. You can see the results of one of such calls in "DeepL_example_output.json" The argument `wait_time` is the time (in seconds) Selenium should wait before parsing the results. This has to be long enough for the page to load the translations. In my experience 1s is more than enough. If you set this value to small you might get results from a previous call of the function or an empty result.
In both cases the driver argument is (the same) selenium.webdriver instance.