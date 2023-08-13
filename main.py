import schedule
from config import SENDING_TIME, TELEGRAM_API_KEY, TELEGRAM_CHAT_ID
from telebot import TeleBot
import requests as r
from bs4 import BeautifulSoup

RANDOM_COMIC_LINK = "https://c.xkcd.com/random/comic/"

bot = TeleBot(TELEGRAM_API_KEY)

def get_comic_data():
    comic_link = r.get(RANDOM_COMIC_LINK).url
    res = r.get(comic_link)
    s = BeautifulSoup(res.content, 'html.parser')
    res = s.find_all('img')[2]
    print(comic_link)
    # print(res.status_code)
    # print(res['src'])
    # print(res['title'])
    # print(res['src'][2:], res['title'])
    number = comic_link.split("/")[-2]
    url = res['src'][2:]
    title = res['title']
    return url, title, number

def send_daily_comic():
    data = get_comic_data()
    text = "Good Morning! Your daily comic is " + data[2]
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="-"*50)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=data[0])
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=data[1])


schedule.every().day.at(SENDING_TIME).do(send_daily_comic)

while True:
    schedule.run_pending()
