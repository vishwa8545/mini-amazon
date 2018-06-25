from flask import send_from_directory,render_template
from amazon.models import users
from amazon.models import db

def __search_by_name(name):
    user = {
        'username':name
    }

    matches = db['users'].find(user)
    if matches.count()>0:
        return matches.next()
    else :
        return None

def signup(name,username,password):
    existing_user = __search_by_name(username)
    if existing_user is not None:
        return False
    else:
        user = {
        'name': name,
        'username': username,
        'password': password
        }
        db['users'].insert_one(user)
        return True
def athuonticate(username,password):

    user = __search_by_name(username)
    if user is None:
        # user does not exist
        return False

    if user['password'] == password:
        # user exists and correct password
        return True
    else:
        return False
