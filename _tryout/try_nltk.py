from urllib import urlopen
import nltk

__author__ = 'Peipei YI'

url = 'http://snap.stanford.edu/data/index.html'
html = urlopen(url).read()
raw = nltk.clean_html(html)
print raw

url = 'http://help.jd.com/help/question-61.html#help1309'
html = urlopen(url).read().decode('gbk')
raw = nltk.clean_html(html)
print raw
