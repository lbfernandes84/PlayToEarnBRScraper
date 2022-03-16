from bs4 import BeautifulSoup

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

import time
import config

class P2EGame:

    def __init__(self):
        self.name = ''
        self.short_description =''
        self.description = ''
        self.twitter = ''
        self.discord_server =''
        self.website =''
        self.genre = []
        self.blockchain = []
        self.devices = []
        self.support_to_nft = False
        self.free_to_play = []

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)

def collect_p2e_games_list(driver, url):
    links =[]
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', class_="table table-bordered mainlist")
    all_games = table.find_all('a', class_='dapp_detaillink socialscoregraph')    
    for game in all_games:
        links.append(game['href'])
        print(links[-1])
    return links

if __name__ == '__main__':
    driver = create_driver()
    collect_p2e_games_list(driver, config.MAIN_URL)