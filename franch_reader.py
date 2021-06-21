import requests
from bs4 import BeautifulSoup as bs

def get_FranchWordList():
    r = requests.get('https://takelessons.com/live/french/useful-french-phrases-travelers-z04')
    soup = bs(r.text)
    ps = soup.findAll('p')
    buf = []
    for e in ps:
        if e.em is not None:
            buf.append((e.em.text,e.contents[-1]))
    return buf


def test():
    for e in buf:
        print(e)

