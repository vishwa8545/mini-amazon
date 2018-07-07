from amazon.models import db
import pymongo
from bson.objectid import ObjectId

def search_one(name):

    maches = db['products'].find(name)
    maches.sort([('price',pymongo.ASCENDING)])
    return list(maches)

def get_detais(p_id):

    cursor = db['products'].find(p_id)
    if cursor.count() == 1:
        return cursor[0]
    else:
        False

def add_one(prod):
    sucess = db['products'].insert_one(prod)
    if sucess:
        return True
    else:
        return False

def update_one(filter,update):
    filter = {'_id':ObjectId(filter)}
    sucess = db['products'].update_one(filter,update)
    if sucess:
        return True
    else:
        return False
def delete_one(filter):
    sucess = db['products'].delete_one(filter)
    if sucess:
        return True
    else:
        False