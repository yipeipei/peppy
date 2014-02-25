import os
import datetime

from _exp.dataset import db


__author__ = 'Peipei YI'

coll_graph = db.graph

snap = 'D:/data/dataset/snap/'
pages = snap + 'pages/'
source = 'snap'

# print int('88,234'.replace(',', ''))
# print '{:,}'.format(1234567890)
# '1,234,567,890'

# tmp = os.path.expanduser('~/Desktop/tmp/')
tmp = 'D:/data/tmp/'
if not os.path.exists(tmp):
    os.makedirs(tmp)

# raw = nltk.clean_html(urlopen(snap_index).read())
# print raw


def extract_index(index):
    """
    extract info from index.html
    """
    category_flag = False
    category = None
    attr = None
    data = None
    with open(index) as f:
        for line in f:
            line = line.strip()
            if line.find('\t') == -1:
                category = line
                category_flag = True
            else:
                if category_flag:
                    attr = line.split('\t')
                    category_flag = False
                else:
                    data = line.split('\t')
                    info = {'date': datetime.datetime.now(),
                            'source': source,
                            'tag': ['official', 'index'],
                            'category': category,
                            'log': 'extract from official index of snap'}
                    detail = dict(zip(attr, data))
                    info.update(detail)
                    coll_graph.insert(info)
                    # print data[0]


def extract_official(page):
    """
    extract info from dataset.html
    """
    with open(page) as f:
        for line in f:
            pass


def unify(dataset):
    """
    unify dataset
    """
    pass


if __name__ == '__main__':
    # process index.html
    index = pages + 'index.html'
    extract_index(index)