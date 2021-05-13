import requests
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

data = tester()
