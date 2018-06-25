from flask import request,jsonify,send_from_directory,render_template
from amazon import app
from amazon.models import products,users



@app.route('/api/product', methods=['GET' , 'POST'])
def product():
    if request.method == 'GET':
        query ={
            'name':request.args['product_name']
        }
        matching_product =products.search_one(query)
        return render_template('results.html',query=query,results=matching_product)





    elif request.method == 'POST':

        name = request.form['name']
        disc = request.form['disc']
        price = request.form['price']
        prod = {
            'name': name,
            'desc': disc,
            'price': price
        }
        if request.form['op_type'] == 'insert':

            sucess = products.add_one(prod)
            if sucess:
                return send_from_directory('static', 'admins.html')
            else:
                return send_from_directory('static','adminf.html')

        if request.form['op_type'] == 'update':
            filter = {
                'name':name
            }

            updates = {

                'desc':disc,
                'price':price
            }

            update = {
                '$set':updates
            }
            sucess = products.update_one(filter,update)
            if sucess:
                return send_from_directory('static','adminus.html')
            else:
                return send_from_directory('static','adminuf.html')



@app.route('/' , methods=['GET'])
def index():
    return send_from_directory('./static','index.html')


@app.route('/api/user', methods=['GET' , 'POST'])
def user():
    if request.method == 'POST':


        if request.form['op_type'] == 'insert':
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            sucess =users.signup(name,username,password)
            if sucess:
                return send_from_directory('static','index.html')
            else:
                return render_template('userex.html')

        elif request.form['op_type'] == 'login':
            username = request.form['username']
            password = request.form['password']
            sucess = users.athuonticate(username,password)
            if sucess:
                return send_from_directory('static','home.html')
            else:
                return send_from_directory('static','athof.html')


