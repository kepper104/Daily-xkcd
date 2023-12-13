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
    res = s.find_all('img')[1]
    print(comic_link)
    print(res)

    number = comic_link.split("/")[-2]
    url = res['src'][2:]
    title = res['alt']
    body_text = res["title"]
    return url, title, number, body_text


def send_daily_comic():
    url, title, number, body_text = get_comic_data()
    text = (f"Good Morning! Your daily comic is {number} - {title} \n"
            f'Dont forget to solve today\'s <a href="https://www.nytimes.com/games/wordle/index.html">Wordle</a>!')

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode="HTML", disable_web_page_preview=True)
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=url, caption=body_text)


schedule.every().day.at(SENDING_TIME).do(send_daily_comic)

while True:
    schedule.run_pending()
