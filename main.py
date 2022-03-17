from urllib import response
import requests
from bs4 import BeautifulSoup


import time
import config

SUCCESSFULL_REQUEST_STATUS = 200

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

def connect_to_source(url):
    r = requests.get(url)
    soup = None
    if r.status_code == SUCCESSFULL_REQUEST_STATUS:  
        soup = BeautifulSoup(r.text, 'html.parser')
    return r.status_code, soup

def collect_p2e_games_list(soup):
    links =[]    
    table = soup.find('table', class_="table table-bordered mainlist")
    all_games = table.find_all('a', class_='dapp_detaillink socialscoregraph')    
    for game in all_games:
        links.append(game['href'])
        # print(links[-1])
    return links

if __name__ == '__main__':
    url = config.MAIN_URL
    status = SUCCESSFULL_REQUEST_STATUS
    all_links = []
    while url is not None:
        status, soup = connect_to_source(url)
        all_links.extend(collect_p2e_games_list(soup)) 
        next_link = soup.find('a', class_="page-link", rel='next')
        print('status: ', status)
        print('next_link: ', next_link)
        if next_link:
            url = next_link['href']
        else:
            url = None
    print('Number of games: ',len(all_links))
    for link in all_links:
        print(link)