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

# Langenscheidt [(https://en.langenscheidt.com/)](https://en.langenscheidt.com/)
Last tested: 22.06.22

## Requirements
- bs4
## Usage
The two main functions are:
- `get_vocab_links_for_language_pair(language_pair)` - This function will collect all links to specific entries in the dictionary for the language pair. Since it has to go through many, many pages to do so this can - depending on which language pair you choose - take quite some time (15' for me with `["german", "english"]`). `language_pair` is an array of tuple of by Langenscheidt supported languages (call  `get_all_language_pairs` to get a list of them.)
- `scrape_examples(link)` - Given a specific link this function will return all the listed examples on the page. Note that it expects you to only give the part after the domain name `langenscheidt.com` (including the backslash), the same way that `get_vocab_links_for_language_pair` returns the links. So e.g. `scrape_examples("/german-english/liebe")` to get the results for the German word for "love". The main focus of my research was to just collect several examples of the word being used, so currently there is no parsing of anything like the type of word or alike. You can find an examples output under Langenscheidt_example_out.json. Alternatively, you can just run `python scrape_Langenscheidt.py`.