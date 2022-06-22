import requests
from bs4 import BeautifulSoup

def get_all_language_pairs():
    page = requests.get("https://en.langenscheidt.com/").text
    soup = BeautifulSoup(page)

    languages = []

    for x in soup.select("span.label"):
        x.find("span").insert_after(" ")
        languages.append([y.strip() for y in x.text.split(" ") if y != ""])

    return languages

def get_vocab_links_for_language_pair(language_pair):
    word_urls = []
    
    start_page_soup = BeautifulSoup(requests.get(
        f"https://en.langenscheidt.com/{'-'.join(language_pair).lower()}"
    ).text)
    
    paths = [x["href"] for x in start_page_soup.select("div.sitemap a")]
    
    letter_urls = [
        f"https://en.langenscheidt.com{P}"
        for P in paths
    ]

    for u in letter_urls:
        i = 0

        while True:
            i += 1
            page = requests.get(f"{u}{i}").text
            soup = BeautifulSoup(page)
            new = [x["href"] for x in soup.select("div.sitemap ul li a")]
            if len(new) == 0:
                break
            word_urls += new
    
    return word_urls

def scrape_examples(link):
    try:
        page = requests.get(f"https://en.langenscheidt.com{link}").text
        soup = BeautifulSoup(page)
        
        col_1 = soup.select(".col1")
        col_2 = soup.select(".col2")

        res = []
        for i in range(len(col_1)):
            col_1_text = [x["data-text"] for x in col_1[i].select(".text-to-speech")]
            col_2_text = [x["data-text"] for x in col_2[i].select(".text-to-speech")]

            if (len(col_1_text) > 0 and len(col_2_text) > 0):
                res.append([col_1_text, col_2_text[0]])

        return [f"https://en.langenscheidt.com{link}", res]
    
    except:
        print("Failed Link:", link)
        return False

import json
if __name__ == "__main__":
    print("All language pairs:")
    print(get_all_language_pairs())

    print("All vocab links:")
    print(get_vocab_links_for_language_pair(["German", "English"])) # might take some time

    print("Example for 'liebe' (German for 'love'):")
    print(scrape_examples("/german-english/liebe"))
    