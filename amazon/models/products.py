from amazon.models import db
import pymongo

def search_one(name):

    maches = db['mini-amazon'].find(name)
    maches.sort([('price',pymongo.ASCENDING)])
    return list(maches)

def get_detais(p_id):
    cursor = db['mini-amazon'].find(p_id)
    if cursor.count() == 1:
        return cursor[0]
    else:
        False

def add_one(prod):
    sucess = db['mini-amazon'].insert_one(prod)
    if sucess:
        return True
    else:
        return False

def update_one(filter,update):
    sucess = db['mini-amazon'].update_one(filter,update)
    if sucess:
        return True
    else:
        False