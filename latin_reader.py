from bs4 import BeautifulSoup as bs

def get_tables(f):
    soap = bs(f, features="html.parser")
    return soap.findAll('table')

def get_words(tables):
    res = []
    for i in range(1,25):
        table = tables[i]
        res.append(get_words_table(table.findAll('tr')))
    return res

def get_words_table(trs):
    res = []
    for i in range(1,len(trs)):
        tr = trs[i]
        if tr.i is not None:
            word = tr.i.getText()
            trans = tr.findAll('td')[1].string
            if trans is not None and word is not None:
                res.append((word,trans))
        elif tr.a is not None:
            word = tr.a.getText()
            trans = tr.findAll('td')[1].string
            if trans is not None and word is not None:
                res.append((word,trans))
    return res

def process():
    fileName = 'latin_full.html'
    f = open(fileName,'r')
    word_list = get_words(get_tables(f))
    f.close()
    return word_list

def checker(word_list):
    for e in word_list:
        for t in e:
            if t[0] is None or t[1] is None:
               return -1
    return 0
if __name__ == '__main__':
    word_list = process()
    if checker(word_list) == 0:
        print("processing successfully")
    else:
        print("processing failed")
