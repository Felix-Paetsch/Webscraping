from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json
import os

# Some part of the Selenium-API I use is depricated
import warnings
warnings.filterwarnings("ignore")

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

if CONFIG["max_images_displayed"] >= 0:
    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": CONFIG["max_images_displayed"]}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": CONFIG["max_images_displayed"]}
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=option)

else:
    driver = webdriver.Chrome("chromedriver.exe")

driver.get("https://discord.com/channels/@me")

def get_all_current_img_links(src = driver.page_source):
    soup = BeautifulSoup(src)
    link_list = soup.select('ol[role=list][data-list-id=chat-messages] > li a')

    res = []
    for x in link_list:
        try:
            if x["href"].split(".")[-1] in CONFIG["valid_file_extensions"]:
                res.append(x["href"][39:])
        except:
            pass
    
    return res

def focus_on_div(driver):
    driver.find_element_by_css_selector('ol[role=list][data-list-id=chat-messages]').click()
       
def perform_scroll(driver):
    el=driver.find_element_by_css_selector('main > div > div[dir=ltr][data-jump-section=global][role=group]')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(el, el.size["width"] - 2, 1)
    action.click()
    action.perform()

def scroll(driver, n, d):
    for _ in range(n):
        perform_scroll(driver)
        time.sleep(d/1000)
        
def get_links_from_scroll_cycle(driver, n, d, stop_after):
    links = get_all_current_img_links(driver.page_source)
    for i in range(stop_after):
        scroll(driver, n, d)
        links += get_all_current_img_links(driver.page_source)
        
    return links

def save_links_from_k_stop_cycles(driver, init_scroll, cycle_save_amt, scroll_pause, stop_after, k, save_dir, prefix):
    try:
        os.mkdir(save_dir)
    except:
        pass
    
    scroll(driver, init_scroll, scroll_pause)
    
    if k > -1:
        for i in range(k):
            with open(f"{ save_dir }/{ prefix }_{ i }.json", 'w', encoding ='utf8') as json_file:
                json.dump(get_links_from_scroll_cycle(driver, cycle_save_amt, scroll_pause, stop_after), json_file)
        
    else:
        i = 0
        while True:
            with open(f"{ save_dir }/{ prefix }_{ i }.json", 'w', encoding ='utf8') as json_file:
                json.dump(get_links_from_scroll_cycle(driver, cycle_save_amt, scroll_pause, stop_after), json_file)
            i += 1

    print("done!")

print("Please navigate to the channel you want to scrape! [Enter]")
print("==========================================================")
input()

save_links_from_k_stop_cycles(driver, 
                              init_scroll = CONFIG["init_scroll"], # how many times to scroll before recording starts
                              cycle_save_amt = CONFIG["cycle_save_amt"], # how many times to scroll before looking for all images on page
                              scroll_pause = CONFIG["scroll_pause"], # how long to wait between each scroll call [in ms]
                              stop_after = CONFIG["cycle_stop_after"], # stop after how many steps a scroll cycle is
                              k = CONFIG["cycle_amt"], # how many scroll cycles?
                              save_dir = CONFIG["save_dir"],
                              prefix=CONFIG["prefix"])