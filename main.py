import os
import telebot
import requests
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

API_key = os.environ['API_key']
# COVID_API_KEY = os.environ['COVID_API_KEY']
bot = telebot.TeleBot(API_key)

url = "https://covid-19-statistics.p.rapidapi.com/reports"

headers = {
    'x-rapidapi-key': "fd0a050648msh4edbe4e85b03f1fp112b67jsndca9be56e3ba",
    'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com"
    }

@bot.message_handler(commands=['Greet', 'Hello'])
def greet(message):
  bot.reply_to(message, 'Hi, this is kyudai TG group bot!')

@bot.message_handler(commands=['淦'])
def gan(message):
  bot.send_message(message.chat.id, getName(message) +'觉得很淦!')

@bot.message_handler(commands=['COVID','corona','コロナ'])
def getCOVID(message):
  # r = requests.get('https://api.opendata.go.jp/fukuoka-shi/patients-summary?apikey='+COVID_API_KEY)
  oneday = timedelta(hours=24)
  today = datetime.today()
  today_s = str(today).split(' ')[0]
  counter = 0
  data_buf = []
  while(True):
    curr_day = today - oneday
    querystring = {"date":str(curr_day).split(' ')[0],"q":"Japan Fukuoka"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    if len(response.json()['data']) != 0:
      data_buf.append(response.json()['data'])
      counter += 1
      if counter == 2:
        break
    today = curr_day
  res_str = '日期：'+ str(data_buf[0][6]['date']) + '，确诊总数：' + str(data_buf[0][6]['confirmed']) + '，较上日增长：' + str(data_buf[0][6]['confirmed_diff']) + '\n地区：' + str(data_buf[0][6]['region'])
  bot.send_message(message.chat.id, res_str)

@bot.message_handler(commands=['透','艹'])
def findMessage(message):
  tmp = message.text.split(' ')
  verb = tmp[0][1:]
  if len(tmp) == 1:
    bot.send_message(message.chat.id, getName(message) +verb+'了自己。')
  if len(tmp) == 2:
    bot.send_message(message.chat.id, getName(message) + verb + '了'+tmp[1]+'。')
  
@bot.message_handler(commands=['news'])
def command_news(message):
	bot.send_message(message.chat.id, "🆕 Latest BBC article:\n")
	bot.send_message(message.chat.id, get_article(), parse_mode='HTML')


def getName(message):
  res = ''
  if message.from_user.first_name != None:
    res += message.from_user.first_name
  if message.from_user.last_name != None:
    res += message.from_user.last_name
  return res

def get_article():
    bbc_request = requests.get('https://www.bbc.com/news')
    soup = BeautifulSoup(bbc_request.text, "html.parser")
    raw_article = soup.find_all('div', {'class': 'gs-c-promo-body gel-1/2@xs gel-1/1@m gs-u-mt@m'})[0].find_all(text=True, recursive=True)
    if raw_article[0].startswith('Video'): #Cheking if article has video and then moving index by 1 for proper display in message
        topic = raw_article[5]
        title = raw_article[1]
        description = raw_article[2]
        publish_time = raw_article[4]
    else:
        topic = raw_article[4]
        title = raw_article[0]
        description = raw_article[1]
        publish_time = raw_article[3]
    href = soup.find_all('div', {'class': 'gs-c-promo-body gel-1/2@xs gel-1/1@m gs-u-mt@m'})[0].find('a', {'class': 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'})['href']
    link = f' https://www.bbc.com{href}'
    article = f'✏️ <b>Topic</b>:  {topic}\n⚠️ <b>Title</b>:  {title}\n📌 <b>Description</b>:  {description}\n🕒 <b>Published</b>:  {publish_time}\n➡️ <b>Full article</b>: {link}'
    return article

bot.polling()