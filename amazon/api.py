from flask import request,jsonify,send_from_directory,render_template,session
from amazon import app
from amazon.models import products,users
from bson.objectid import ObjectId


@app.route('/api/product', methods=['GET' , 'POST'])
def product():
    if request.method == 'GET':
        query ={
            'name':request.args['name']
        }
        matching_product =products.search_one(query)
        query = request.args['name']
        return render_template('adminresults.html',query=query,results=matching_product)





    elif request.method == 'POST':


        if request.form['op_type'] == 'insert':
            name = request.form['name']
            disc = request.form['disc']
            price = request.form['price']

            prod = {
                'name': name,
                'desc': disc,
                'price': price
            }

            sucess = products.add_one(prod)
            if sucess:
                return render_template( 'admin.html',massage = 'product added successfully')
            else:
                return render_template( 'admin.html',massage = 'product not added')

        if request.form['op_type'] == 'update':
            name = request.form['name']
            disc = request.form['disc']
            price = request.form['price']

            prod = {
                'name': name,
                'desc': disc,
                'price': price
            }
            product_id = request.form['product_id']
            filter = product_id

            updates = {
                'name':name,
                'desc':disc,
                'price':price
            }

            update = {
                '$set':updates
            }
            sucess = products.update_one(filter,update)
            if sucess:
                return render_template('admin.html', massage = 'the product is updated sucessfully')
            else:

                return render_template('admin.html', massage = 'the product is not updated')

        if request.form['op_type'] == 'delete':
            product_id = request.form['product_id']
            filter = {'_id':ObjectId(product_id)}
            sucess = products.delete_one(filter)
            if sucess:
                return render_template('admin.html',massage = 'the product is deleted sucessfully')
            else:
                return render_template('admin.html', massage='unable to delete the product')


@app.route('/' , methods=['GET'])
def index():
    if 'user_id' in session:

        name = users.search_by_user_id(session['user_id'])
        return render_template('home.html',name=name['name'])
    else:
        return render_template('user.html',massage ='10% off on paypal payments')
@app.route('/admin' , methods=['GET'])
def admin():
    return render_template('admin.html',massage = 'welcome admin')
@app.route('/logout', methods = ['GET'])
def logout():
    del session['user_id']
    return render_template('user.html', massage = 'u have sucessfully logged out')



@app.route('/api/user', methods=['GET' , 'POST'])
def user():
    if request.method == 'POST':


        if request.form['op_type'] == 'insert':
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            sucess =users.signup(name,username,password)
            if sucess:
                if username == 'admin':
                    user = users.search_by_name(username)
                    session['user_id'] = str(user['_id'])
                    return render_template('admin.html', massage = "wellcome admin")
                else:
                    return render_template('home.html', massage = 'the signup was successfull')
            else:
                return render_template('user.html', massage = 'the username already present')

        elif request.form['op_type'] == 'login':
            username = request.form['username']
            password = request.form['password']
            sucess = users.athuonticate(username,password)
            if sucess:
                if username == 'admin':
                    user = users.search_by_name(username)
                    session['user_id'] = str(user['_id'])
                    return render_template('admin.html', massage="wellcome admin")

                else:
                    user = users.search_by_name(username)
                    session['user_id'] = str(user['_id'])
                    return render_template('home.html', name = user['name'])
            else:
                return render_template('user.html', massage = 'invalid username/passsword')


@app.route('/api/cart',methods =['POST'])
def cart():
    op_type = request.form['op_type']
    if op_type == 'add':

        user_id = session['user_id']
        product_id = request.form['product_id']
        sucess =users.add_to_cart(user_id,product_id)
        if sucess:
            return render_template('home.html',name = 'the product added to card sucessfully')
        else:
            return render_template('home.html',name = 'the product is nopt added to cart')
    if op_type == 'retrive':
        user_id = session['user_id']
        product_ids = users.retrive_cart(user_id)
        cart = []
        name = users.search_by_user_id(user_id)
        for p_id in product_ids:
            product_id = {'_id':ObjectId(p_id)}
            cart.append(products.get_detais(product_id))
        return render_template('cart.html', results =cart,name = name['name'])
    if op_type == 'delete':
        user_id = session['user_id']
        product_id = request.form['product_id']
        sucess = users.remove_cart(user_id,product_id)
        if sucess:

            product_ids = users.retrive_cart(user_id)
            cart = []
            name = users.search_by_user_id(user_id)
            for p_id in product_ids:
                product_id = {'_id': ObjectId(p_id)}
                cart.append(products.get_detais(product_id))
            return render_template('cart.html', results=cart, name=name['name'])
        else:
            return render_template('home.html',name = 'the product is not deleterd from the cart')