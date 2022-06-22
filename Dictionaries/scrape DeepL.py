from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

def set_languages(driver, source_lan, target_lan):
    driver.get(f"https://www.deepl.com/translator#{ source_lan }/{ target_lan }/random_input")

def get_data_for_word(driver, text, wait_time):
    def make_input(driver, inp):
        ta = driver.find_elements(by=By.CSS_SELECTOR, value="div.lmt__inner_textarea_container textarea")[0]
        ta.send_keys(Keys.CONTROL, 'a')
        ta.send_keys(inp) 

    def get_translation(driver):
        ta = driver.find_elements(by=By.CSS_SELECTOR, value='textarea')[1]
        return ta.get_attribute("value").strip()

    def get_suggestions(driver):
        def parse_lemma(x):
            def parse_translation(y):
                def get_example(z):
                    return {
                        "src": z.select("span.tag_s")[0].text,
                        "target": z.select("span.tag_t")[0].text
                    }

                res = {
                    "translation": y.select("span.tag_trans >a")[0].text.strip(),
                    "examples": [get_example(z) for z in y.select("div.example_lines div.example.line > span")]
                }
                placeholder_arr = y.select("span.tag_trans >a > span")
                if len(placeholder_arr) > 0:
                    res["placeholder"] = placeholder_arr[0].text
                    res["translation"] = res["translation"][len(res["placeholder"]):].strip()

                return res

            context_arr = x.select("div > h2 span.tag_lemma_context")
            context = None if len(context_arr) == 0 else context_arr[0].text
            return {
                "main_term": {
                    "text": x.select("div > h2 a.dictLink")[0].text,
                    "context": context,
                    "word_type": x.select("div > h2 span.tag_wordtype")[0].text
                },
                "translations": [parse_translation(y) for y in x.select("div.translation")]
            } 
            
        try:
            exact_list = driver.find_elements(by=By.CSS_SELECTOR, value="div.exact")

            if len(exact_list) == 0:
                return []

            exact = BeautifulSoup(exact_list[0].get_attribute('innerHTML'))
            return [
                parse_lemma(x) for x in exact.select("div.lemma")
            ]

        except:
            return []

    make_input(driver, text)
    time.sleep(max_time)
    return {
        "input": text,
        "translation": get_translation(driver),
        "suggestions": get_suggestions(driver)
    }

if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path="chromedriver.exe")

    set_languages(driver, "en", "nl")
    get_data_for_word(driver, "please", wait_time)