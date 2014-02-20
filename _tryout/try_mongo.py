import datetime
from bson import ObjectId
from pymongo import MongoClient, DESCENDING, ASCENDING

__author__ = 'Peipei YI'



# connect on the default host and port
client = MongoClient()

# connect on a specific host and port
# client = MongoClient('localhost', 27017)

# connect by the MongoDB URI format
# client = MongoClient('mongodb://localhost:27017/')



# get a database by attribute style
db = client.test

# get a database by dictionary style
# db = client['test']



# get a collection
collection = db.test1
# collection = db['test1']

# Databases and collections in MongoDB are created lazily,
# they are created when the first document is inserted into them.



# documents is represented and stored in JSON-style
# use dictionary to represent document
post = {'author': 'Mike',
        'text': 'My first post!',
        'tags': ['mongodb', 'python', 'pymongo'],
        'date': datetime.datetime.now()}
print post
# native python types (like datetime.datetime instance)
# will be automatically converted to and from BSON types.



# insert a document
posts = db.posts
# post_id = posts.insert(post)
# print post_id
# insert() returns the value of "_id"
# when a document is inserted a special key, "_id", is automatically added
# if the document doesn't already contain an "_id" key.
# "_id" must be unique across the collection.



# list all collections
print db.collection_names()

# [u'system.indexes', u'posts']



# get a single document
print posts.find_one()

# {u'date': datetime.datetime(2014, 2, 20, 21, 18, 31, 651000),
#  u'text': u'My first post!',
#  u'_id': ObjectId('530600a77c7a1e3524b24dca'),
#  u'author': u'Mike',
#  u'tags': [u'mongodb', u'python', u'pymongo']}

# MongoDB stores data in BSON format.
# BSON strings are UTF-8 encoded
# so PyMongo must ensure that any strings it stores
# contain only valid UTF-8 data.
# Relgular strings (<type 'str'>) are validated and stored unaltered.
# Unicode strings (<type 'unicode'>) are encoded UTF-8 first.
# The reason why we get u'Mike' back is that
# PyMongo decodes each BSON string into a Python unicode string, not a regular str.


print posts.find_one({'author': 'mike'})
# None



# query by ObjectId, not just its string representation
post_id = ObjectId('53060f1b7c7a1e4d98b785e7')
print posts.find_one({'_id': post_id})



# bulk insert, by passing it an iterable
new_posts = [{'author': 'Mike',
              'text': 'Another post!',
              'tags': ['bulk', 'insert'],
              'date': datetime.datetime.now()},
             {'author': 'Eliot',
              'title': 'MongoDB is fun', # MongoDB is schema-free
              'text': 'and pretty easy too!',
              'date': datetime.datetime(2012, 12, 20)}]
# post_ids = posts.insert(new_posts)
# print post_ids
# [ObjectId('53060f677c7a1e3ab8e1a1d2'), ObjectId('53060f677c7a1e3ab8e1a1d3')]



# query for more than one document, find() returns a Cursor instance, allows iterate
print 'query for more than one document'
# for post in posts.find():
for post in posts.find({'author': 'Mike'}):
    print post



# counting, just want to know how many documents match a query
print posts.count()   # count of all documents in a collection
print posts.find({'author': 'Mike'}).count()    # count of matched document



# range queries, using {'$gt': d}
d = datetime.datetime(2012, 12, 30)
for post in posts.find({'date': {'$gt': d}}).sort('author'):
    print post



# indexing, to make query fast

# using explain() method to get how the query is being performed without the index
# print posts.find({'date': {'$lt': d}}).sort('author').explain()['cursor']
# u'BasicCursor'
# print posts.find({'date': {'$lt': d}}).sort('author').explain()['nscanned']
# 4
# we can that the query is using BasicCursor and scanning all 3 documents in the collection.

# now, let's add a compound index and look at the same information
# print posts.create_index([('date', DESCENDING), ('author', ASCENDING)])
# u'date_-1_author_1'

# try explain() again
# print posts.find({'date': {'$gt': d}}).sort('author').explain()['cursor']
# CAUTIOUS: $gt might cause OverflowError: Python int too large to convert to C long

print posts.find({'date': {'$lt': d}}).sort('author').explain()['cursor']
# u'BtreeCursor date_-1_author_1'
print posts.find({'date': {'$lt': d}}).sort('author').explain()['nscanned']
# 1
