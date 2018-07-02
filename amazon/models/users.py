from flask import send_from_directory,render_template
from amazon.models import users
from amazon.models import db
from bson.objectid import ObjectId


def search_by_name(name):
    user = {
        'username':name
    }

    matches = db['users'].find(user)
    if matches.count()>0:
        return matches.next()
    else :
        return None

def search_by_user_id(user_id):
    user = {
        '_id':ObjectId(user_id)
    }

    matches = db['users'].find(user)
    if matches.count()>0:
        return matches.next()
    else :
        return None

def signup(name,username,password):
    existing_user = search_by_name(username)

    if existing_user is not None:
        return False
    else:
        user = {
        'name': name,
        'username': username,
        'password': password,
        'cart':[]
        }
        db['users'].insert_one(user)
        return True
def athuonticate(username,password):

    user = search_by_name(username)
    if user is None:

        return False

    if user['password'] == password:

        return True
    else:
        return False

def add_to_cart(user_id,product_id):
    condition = {'_id':ObjectId(user_id)}

    cursor = db['users'].find(condition)
    if cursor.count() == 1:
         user_data = cursor[0]
    else :
        return False

    if 'cart' not in user_data:
        user_data['cart'] = []


    if product_id not in user_data['cart']:
        user_data['cart'].append(product_id)
        db['users'].update_one(filter = condition,update={'$set':user_data})
        return True
    else:
        return False

def retrive_cart(user_id):
    condition = {'_id': ObjectId(user_id)}

    cursor = db['users'].find(condition)
    if cursor.count() == 1:
        return cursor[0]['cart']
    else:
        return False
