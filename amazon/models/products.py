from amazon.models import db

def search_one(name):

    maches = db['mini-amazon'].find(name)
    return list(maches)
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