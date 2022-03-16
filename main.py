from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

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
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)

def collect_data(driver, url):
    pass

if __name__ == '__main__':
    create_driver