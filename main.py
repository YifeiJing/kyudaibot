import os
import telebot
import requests

API_key = os.environ['API_key']
COVID_API_KEY = os.environ['COVID_API_KEY']
bot = telebot.TeleBot(API_key)

@bot.message_handler(commands=['Greet', 'Hello'])
def greet(message):
  bot.reply_to(message, 'Hi, this is kyudai TG group bot!')

@bot.message_handler(commands=['淦'])
def gan(message):
  bot.send_message(message.chat.id, getName(message) +'觉得很淦!')

@bot.message_handler(commands=['COVID','corona','コロナ'])
def getCOVID(message):
  r = requests.get('https://api.opendata.go.jp/fukuoka-shi/patients-summary?apikey='+COVID_API_KEY)
  bot.send_message(message.chat.id, r.text)

@bot.message_handler(commands=['透','艹'])
def findMessage(message):
  tmp = message.text.split(' ')
  verb = tmp[0][1:]
  if len(tmp) == 1:
    bot.send_message(message.chat.id, getName(message) +verb+'了自己。')
  if len(tmp) == 2:
    bot.send_message(message.chat.id, getName(message) + verb + '了'+tmp[1]+'。')

def getName(message):
  res = ''
  if message.from_user.first_name != None:
    res += message.from_user.first_name
  if message.from_user.last_name != None:
    res += message.from_user.last_name
  return res

bot.polling()