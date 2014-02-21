import os
from urllib import urlopen
from bs4 import BeautifulSoup

import nltk

from _exp.dataset import db

__author__ = 'Peipei YI'

collection = db.graph

source = 'snap'
snap_index = 'https://snap.stanford.edu/data/egonets-Facebook.html'


# print int('88,234'.replace(',', ''))
# print '{:,}'.format(1234567890)
# '1,234,567,890'

# tmp = os.path.expanduser('~/Desktop/tmp/')
tmp = 'D:/data/tmp/'
if not os.path.exists(tmp):
    os.makedirs(tmp)


raw = nltk.clean_html(urlopen(snap_index).read())
print raw
# open(tmp + "raw", 'w+').write(raw)



# soup = BeautifulSoup(urlopen(snap_index).read())

# with open("example.txt", "w") as f:
#     f.write(soup.get_text())
# print soup.get_text()