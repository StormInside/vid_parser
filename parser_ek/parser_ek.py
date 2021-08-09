from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import random

link = "https://ek.ua/ek-list.php?katalog_=189&search_=6600+xt"


def get_html(url = link, proxy = False):

    if proxy:
        pass
    else:
        try:
            response = requests.get(url)
            print(f"{datetime.now()} = ek = {response.status_code}")
            if(int(response.status_code)!=200):
                f=open('errors.txt', "a")
                f.write(f"{datetime.now()} = ek = {response.status_code}\n")
                f.close()

            return response.content
        except Exception as ex:
            response = requests.get(url)
            f=open('errors.txt', "a")
            f.write(f"{datetime.now()} = ek = {response.status_code} = {ex}\n")
            f.close()
            print(ex)


def parse_html(content = None):

    if not content:
        content = get_html()


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
            f=open('ok.txt', "a")
            f.write(f"{datetime.now()} = ek = {link} = {price}\n")
            f.close()

def send_data(text):
    try:
        r = requests.get(url = f'http://192.168.0.150:5000/message?text={text}')
        res = r.json()
        # print(res)
        if res["ok"] != True:
            print("FAILED TO SEND DATA")
            f=open('errors.txt', "a")
            f.write(f"{datetime.now()} = ek = FAILED TO SEND DATA\n")
            f.close()
    except Exception as ex:
        f=open('errors.txt', "a")
        f.write(f"{datetime.now()} = ek = {text} = {ex}\n")
        f.close()
        print(ex)
        time.sleep(1)
        send_data(text)


def runner():
    while True:
        parse_html()
        time.sleep(random.randint(2,12))


runner()