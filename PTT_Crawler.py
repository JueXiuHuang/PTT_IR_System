import multiprocessing
import configparser
import requests
import json
from selenium import webdriver
from lxml import etree
#from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Pool

def fetch_artical(url):
    d = {}
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    content = BeautifulSoup(resp.text, 'html.parser')

    # get the information of board, artical title, author
    if content.select_one('#topbar > a.board > span') != None:
        content.select_one('#topbar > a.board > span').decompose()
    board = ''
    if content.select_one('#topbar > a.board') != None:
        board = content.select_one('#topbar > a.board').getText()
    title = ''
    if content.select_one('#main-content > div:nth-child(3) > span.article-meta-value') != None:
        title = content.select_one('#main-content > div:nth-child(3) > span.article-meta-value').getText()
    author = ''
    if content.select_one('#main-content > div:nth-child(1) > span.article-meta-value') != None:
        author = content.select_one('#main-content > div:nth-child(1) > span.article-meta-value').getText()
    
    # remove pushes and other unimportant information
    content = content.select_one('#main-content')
    if content == None:
        print(url)
    for metaline in content.find_all('div', class_='article-metaline'):
        metaline.decompose()
    if content.select_one('#main-content > div.article-metaline-right') != None:
        content.select_one('#main-content > div.article-metaline-right').decompose()
    pushes = content.find_all('div', class_='push')
    for p in pushes:
        p.decompose()
    
    # get the artical
    artical = content.getText()

    json_data = {'board':board, 'title':title, 'author':author, 'artical':artical}

    return json_data

# not support over18 verification
if __name__ == '__main__':
    base = 'https://www.ptt.cc'
    bar_f='{desc:<5.5}{percentage:3.0f}%|{bar:50}{r_bar}'

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    pages = int(config['setting']['pages'])
    boards_list = []
    arti_list = []
    for b in config['URL']:
        boards_list.append(config['URL'][b])
    
    for url in boards_list:
        for p in tqdm(range(pages), bar_format='{desc:<5.5}{percentage:3.0f}%|{bar:50}{r_bar}'):
            resp = requests.get(url)
            next_page_url = etree.HTML(resp.text).xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]/@href')[0]
            url = base+next_page_url
            content = BeautifulSoup(resp.text, 'html.parser')
            li = content.find_all('div', class_='r-ent')
            for i in li:
                href = i.find('div', class_='title').select_one('a')
                if href == None:
                    continue
                href = base+href.get('href')
                arti_list.append(href)

    mgr = multiprocessing.Manager()
    share_list = mgr.list()
    with Pool(processes=5) as p:
        with tqdm(range(len(arti_list)), bar_format=bar_f) as bar:
            for i, _ in enumerate(p.imap_unordered(fetch_artical, arti_list)):
                json_data = _
                if json_data != None:
                    share_list.append(json_data)
                bar.update()
    
    # write into database
    with open('crawled_data_latest.json', 'w', encoding='utf-8') as f:
        for i in share_list:
            json_str = json.dumps(i, ensure_ascii=False)
            f.write(json_str+'\n')