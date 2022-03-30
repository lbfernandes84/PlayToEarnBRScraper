import string
from urllib import request, response
import requests
from bs4 import BeautifulSoup


import time
import config

SUCCESSFULL_REQUEST_STATUS = 200


class P2EGame:

    def __init__(self):
        self.name = ''
        self.status = ''
        self.short_description = ''
        self.description = ''
        self.social = {'website': '', 'twitter': '', 'discord': ''}
        self.genre = []
        self.blockchain = []
        self.devices = []
        self.support_to_nft = False
        self.free_to_play = []
        self.play_to_earn = []

    def __repr__(self) -> str:
        genre = ', '.join(self.genre)
        blockchain = ', '.join(self.blockchain)
        devices = ', '.join(self.devices)
        play_to_earn = ', '.join(self.play_to_earn)
        return f'Nome: {self.name}\n status: {self.status}\n descrição: {self.description}\n twitter: {self.social["twitter"]}\n discord: {self.social["discord"]}\n website: {self.social["website"]}\n genre: {genre}\n blockchain: {blockchain}\n devices: {devices}\n support nft: {self.support_to_nft}\n Free to play: {self.free_to_play}\n Play to Earn: {play_to_earn}\n'


def connect_to_source(url):
    r = requests.get(url)
    soup = None
    if r.status_code == SUCCESSFULL_REQUEST_STATUS:
        soup = BeautifulSoup(r.text, 'html.parser')
    return r.status_code, soup


def collect_p2e_games_list(soup):
    links = []
    table = soup.find('table', class_="table table-bordered mainlist")
    all_games = table.find_all('a', class_='dapp_detaillink socialscoregraph')
    for game in all_games:
        links.append(game['href'])
        # print(links[-1])
    return links


def collect_p2e_games_details(p2e_links):
    for link in p2e_links:
        r = requests.get(link)
        if r.status_code == SUCCESSFULL_REQUEST_STATUS:
            soup = BeautifulSoup(r.text, 'html.parser')

            p2egame = P2EGame()
            # nft game name
            div = soup.find('div', class_='headline-dapp')
            p2egame.name = div.find('h1').string

            # nft status
            p2egame.status = soup.find('a', class_='status').string

            # nft game description
            print("Description: ", soup.find_all('p')[2])
            p2egame.description = soup.find('p').string

            # nft game genre
            div = soup.find('div', class_='dapp_categories')
            genre = div.find_all('a')
            p2egame.genre = [a.string for a in genre]

            # nft game blockchain
            div = soup.find('div', class_='dapp_platforms')
            platforms = div.find_all('a')
            p2egame.blockchain = [a['title'] for a in platforms]

            # nft game devices
            div = soup.find('div', class_='dapp_devices')
            devices = div.find_all('a')
            p2egame.devices = [a['title'] for a in devices]

            # nft game details
            div = soup.find('div', class_='dapp_nft_p2e')
            subdiv = div.find_all('div')
            if len(subdiv) == 3:
                yes_or_no = subdiv[0].find('a').string
                yes_or_no = yes_or_no.upper()
                yes_or_no = yes_or_no.strip()
                p2egame.support_to_nft = True if yes_or_no == "YES" else False

                p2egame.free_to_play = subdiv[1].find('a').string
                play_to_earn = subdiv[2].find_all('a')
                p2egame.play_to_earn = [a.string for a in play_to_earn]

            # social media details
            div = soup.find('div', class_='social')
            references = div.find_all('a')
            for reference in references:
                subdiv = reference.find('div')
                if len(subdiv['class']) == 3:
                    candidate_key = subdiv['class'][2]
                    if p2egame.social.get(candidate_key) is not None:
                        p2egame.social[candidate_key] = reference['href']
            # print(p2egame)


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
        break
    collect_p2e_games_details(all_links[:10])
    print('Number of games: ', len(all_links))
    for link in all_links:
        print(link)
