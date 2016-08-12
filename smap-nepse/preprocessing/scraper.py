# scrapper engine for stock market analysis and prediction. It fetches the stock
# data from nepalstock.com.np and stores the data company wise. The data is stored
# in a .csv format.

import requests
from bs4 import BeautifulSoup
import os

#stock name and number fetch
index = 1
dictionary = {}

print('{}{}{}'.format('Stock Name', 'Stock Symbol', 'Stock Number'))
stock_symbols = open('stock_symbols.csv', 'w')
stock_symbols.write('{},{},{}\n'.format('Stock Name', 'Stock Symbol', 'Stock Number'))

while index<13:
    r = requests.get('http://nepalstock.com.np/company/index/'+str(index)+'/stock-name//')
    soup = BeautifulSoup(r.content,'html.parser')
    for tr in soup.find_all('tr')[2:]:
        try:
            tds = tr.find_all('td')
            tdl = tds[5].select('a[href]')
            tdl = str(tdl)
            print('{:60.60}{:>20}{:>20}'.format(tds[2].text.strip(), tds[3].text, tdl[69:72]))
            dictionary[tds[3].text]=tdl[69:72]
            stock_symbols.write('{},{},{}\n'.format(tds[2].text.strip(), tds[3].text, tdl[69:72]))
        except:
            pass

    index += 1
stock_symbols.close()

#static parts
part1 = ('http://nepalstock.com.np/main/stockwiseprices/index/0/Date/aesc'
         '/YTo0OntzOjk6InN0YXJ0RGF0ZSI7czoxMDoiMjAxMC0wMS0wMSI7czo3OiJlbmREYXRlIjtzOjA6Ii'
         'I7czoxMjoic3RvY2stc3ltYm9sIjtzOjM6IjIxNiI7czo2OiJfbGltaXQiO3M6MjoiNTAiO30'
         '?startDate=2010-01-01&endDate=&stock-symbol=')
part2 = '&_limit=5000'

#dictionary mend
index = 0
keys = list(dictionary.keys())
keys.sort()
values = []
for key in keys:
    values.append(dictionary[key])
def get(index):
    stock_number = values[index]
    return part1+str(stock_number)+part2


# create a subdirectory 'data' for storing scrapped data if it is not present.
if not os.path.exists('../data'):
    os.mkdir('../data')
os.chdir('../data')

while index<len(dictionary):
    url = get(index)
    r = requests.get(url)
    soup =  BeautifulSoup(r.content,'html.parser')
    with open(keys[index]+'.csv','a')as f:
        print('writing to {}.csv\n'.format(keys[index]))
        f.write("Date,Total Transactions,Traded Shares,TotalTraded Amount,"+
                "Maximum Price,Minimum Price,Closing Price\n")
        for tr in soup.find_all('tr')[2:]:
            tds =  tr.find_all('td')
            try:
                f.write("%s,%s,%s,%s,%s,%s,%s\n"
                        %(tds[1].text, tds[2].text,tds[3].text,tds[4].text,
                          tds[5].text,tds[6].text,tds[7].text))
            except:
                pass
    index += 1
