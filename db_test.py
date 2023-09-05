from pymongo import MongoClient
import urllib, os, pymongo

password = urllib.parse.quote(os.getenv('PASSWORD'))
uri = f'mongodb+srv://Creonnn:{password}@cluster0.3ataaai.mongodb.net/?retryWrites=true&w=majority'
cluster = MongoClient(uri)

db = cluster['discord']
collection = db['roster']

q=collection.find({'char_name':'Yuds'})
collection.update_one({'char_name':'Yuds'}, {'$set':{'ilvl':'1600'}})





#post = {'_id': 751664230964527206}
#collection.insert_one(post)
#for el in collection.find({}):
#    pprint(el)
#print(collection.find_one({'_id': 751664230964527206}))

#how to insert
#{"_id": 0, "name": "yuds", "char": "yuds", "class": "sorc", "ilvl": 1510, "engraving": reflux}
#post = {"_id": 0, "name": "yuds", "char": "yuds", "class": "sorc", "ilvl": '1510', "engraving": 'reflux'}
#collection.insert_one(post)

#insert multiple
#collection.insert_many([post1, post2]
