from typing import Counter
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import time
import random

link_ek = "https://ek.ua/ek-list.php?katalog_=189&search_=6600+xt"
# link_hotline = "https://hotline.ua/computer/videokarty/?q=6600+xt"
link_tele = "https://telemart.ua/search/?search_que=RX+6600+XT"

alert_server_ip = "192.168.0.150:5000"

def write_to_file(text, filename):
    f=open(filename, "a")
    f.write(text)
    f.close()


def get_html(url, proxy = False):

    if proxy:
        pass
    else:
        try:
            response = requests.get(url)
            print(f"{datetime.now()} = {url} = {response.status_code}")
            if(int(response.status_code)!=200):
                write_to_file(f"{datetime.now()} = {url} = {response.status_code}\n", 'errors.txt')

            return response.content
        except Exception as ex:
            response = requests.get(url)
            write_to_file(f"{datetime.now()} = {url} = {ex}\n", 'errors.txt')
            print(ex)


def send_data(text):
    try:
        r = requests.get(url = f'http://{alert_server_ip}/message?text={text}')
        res = r.json()
        # print(res)
        if res["ok"] != True:
            print("FAILED TO SEND DATA")
            write_to_file(f"{datetime.now()} = FAILED TO SEND DATA\n", 'errors.txt')

    except Exception as ex:
        write_to_file(f"{datetime.now()} = {text} = {ex}\n", 'errors.txt')
        print(ex)
        time.sleep(1)
        send_data(text)


def parse_html_ek():

    content = get_html(link_ek)

    soup = BeautifulSoup(content, features="html.parser")
    items = soup.find_all(class_="list-item--goods")
    for item in items:
        info = item.find(class_="model-short-info")
        title = info.find(class_="model-short-title")
        link = "https://ek.ua/" + title['href']
        price = item.find(class_="model-hot-prices-td").text
        if price != "New Новинка ожидается" and price != "Ожидается в продаже":
            print(f"{link} = {price}")
            send_data(f"{link} = {price}")
            write_to_file(f"{datetime.now()} = ek = {link} = {price}\n", 'ok.txt')

def parse_html_tele():
    
    content = get_html(link_tele)

    soup = BeautifulSoup(content, features="html.parser")
    items = soup.find_all(class_="cards__item")
    for item in items:
        info = item.find(class_="b-i-product-inner-b")
        title = info.find(class_="b-i-product-name")
        link = title.find('a')['href']
        price = item.find(class_="b-i-product-mid-meta").text
        if "Нет в наличии" not in price:
            print(f"{link} = {price}")
            send_data(f"{link} = {price}")
            write_to_file(f"{datetime.now()} = tele = {link} = {price}\n", 'ok.txt')


def runner():
    timer = datetime.now()
    counter = 0
    while True:
        tn = datetime.now()
        if tn - timer >= timedelta(hours=1):
            timer = datetime.now()
            write_to_file(f"{tn} -- {counter} times", "logs.txt")

        try:
            parse_html_ek()
            parse_html_tele()

            counter+=1
        except Exception as ex:
            write_to_file(f"{datetime.now()} = {ex}\n", 'errors.txt')
            print(ex)

        
        time.sleep(random.randint(2,12))


runner()