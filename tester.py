import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
url = "https://covid-19-statistics.p.rapidapi.com/reports"

headers = {
    'x-rapidapi-key': "fd0a050648msh4edbe4e85b03f1fp112b67jsndca9be56e3ba",
    'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com"
    }
    
def tester():
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
  return data_buf

def get_schedule(name):
  schedule = []
  with open(name+'.csv', 'r') as f:
    pass

def find_schedule(name):
  today = datetime.today()
  schedule = get_schedule(name)
  weekdays = ['月', '火', '水', '木', '金', '土', '日']
  curr_weekday_num = today.weekday()
  print('Today is ' + weekdays[curr_weekday_num] + '.')
  for i in schedule[curr_weekday_num]:
    print(i)
# data = tester()
def getSource():
  response = requests.get('https://www.pref.fukuoka.lg.jp/contents/covid19-hassei.html')
  soup = BeautifulSoup(response.text, "html.parser")
  return soup
res = getSource()