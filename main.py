import os
import sys
import telebot
import requests
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from franch_reader import get_FranchWordList 
from latin_reader import process
import random

API_key = os.environ['API_key']
# COVID_API_KEY = os.environ['COVID_API_KEY']
bot = telebot.TeleBot(API_key)

url = "https://covid-19-statistics.p.rapidapi.com/reports"

headers = {
    'x-rapidapi-key': "fd0a050648msh4edbe4e85b03f1fp112b67jsndca9be56e3ba",
    'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com"
    }

wordListLatin = process()

def read_franch_list():
    return get_FranchWordList()

wordListFranch = read_franch_list()
@bot.message_handler(commands=['Greet', 'Hello'])
def greet(message):
  bot.reply_to(message, 'Hi, this is kyudai TG group bot!')

@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "Still alive and kicking!")


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
  stream = os.popen('sh myscript.sh')
  output = stream.read()
  output = '昨日地区新增：\n' + output
  bot.send_message(message.chat.id, output)

@bot.message_handler(commands=['bullshit'])
def bullshit(message):
    tmp = message.text.split(' ')
    if len(tmp) == 1 or len(tmp) > 2:
        bot.send_message(message.chat.id, "Usage:\\bullshit [topic]")
        return
    word = tmp[1]
    sh_input = "cd ~/BullshitGenerator && echo \"{w}\" | python3 自动狗屁不通文章生成器.py"
    stream = os.popen(sh_input.format(w=word))
    output = stream.read()
    bot.send_message(message.chat.id, output[8:])


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
@bot.message_handler(commands=['把'])
def let_done(message):
    rm = message.reply_to_message
    if rm is None:
        return
    somebody_name = getName(rm)
    i_name = getName(message)
    tmp = message.text.split(' ')
    if len(tmp) != 2:
        return
    ret = i_name + '把' + somebody_name + tmp[1] + '!'
    bot.send_message(message.chat.id, ret)
@bot.message_handler(commands=['exit'])
def program_exit(message):
    bot.send_message(message.chat.id, 'Bot shut down\n Moriturus te saluto!')
    pid = os.getpid()
    os.system('kill ' + str(pid))
    sys.exit(0)
@bot.message_handler(commands=['latin'])
def produce_latin(message):
    word, trans = get_latin()
    bot.send_message(message.chat.id,'Your Latin phrase:\n ' + word)
    bot.send_message(message.chat.id, 'Meaning:\n '+ trans)
    return

@bot.message_handler(commands=['franch'])
def produce_franch(message):
    phrase = get_franch()
    bot.send_message(message.chat.id,phrase[0])
    bot.send_message(message.chat.id,phrase[1])
    return

def get_latin():
    table = random.choice(wordListLatin)
    while len(table) == 0:
        table = random.choice(wordListLatin)
    return random.choice(table)

def get_franch():
    choice = random.choice(wordListFranch)
    return choice

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
