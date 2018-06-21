from flask import Flask, request, send_from_directory,jsonify

app = Flask('Amazon')


products = []
@app.route('/home', methods=['GET' , 'POST'])
def product():
    if request.method == 'GET':
        query = request.args['product_name']
        for  prob in products:
            if prob['name'] == query:
                return jsonify(prob)
        return "no match"



    elif request.method == 'POST':
        if request.form['op_type'] == 'insert':
            name = request.form['product_name']
            dsc = request.form['product_disc']
            price = request.form['product_price']
            prob = {
                'name':name,
                'desc':dsc,
                'price':price
            }
            products.append(prob)
            return send_from_directory('static','index.html')
        if request.form['op_type'] == 'update':
            for product in products:
                if request.form['name'] == product['name']:
                    product['desc'] = request.form['disc']
                    product['price'] = request.form['price']
                    return jsonify(product)
            return "not updated"


@app.route('/' , methods=['GET'])
def index():
    return send_from_directory('static','index.html')


if __name__ == '__main__':
     app.run(host='0.0.0.0',port=5000)

