# coding:utf-8

# from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, session, redirect, url_for, request, render_template
import numpy as np
import json

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    title = 'ホーム'
    return render_template('index.html', title=title)

@app.route('/form')
def form():
    title = 'ようこそ'

    return render_template('form_input.html',title=title)

@app.route('/post',methods=['GET','POST'])
def post():
    title = 'こんにちは'
    if request.method == 'POST':
        name = request.form['name']
        return render_template('form_input.html', title=title, name=name)

    else:
        return redirect(url_for('index'))

@app.route('/confirm',methods=['POST'])
def confirm():
    title = '注文確認'
    params = {}
    params = request.form
    return render_template('confirm.html',params=params,title=title)

@app.route('/thanks',methods=['POST'])
def thanks():
    return render_template('thanks.html')

@app.route('/product',methods=['GET','POST'])
def product_detail():

    if 'cart_items' not in session:
        session['cart_items'] = []

    cart_list = session['cart_items']
    flg = False
    is_zero = True
    if request.method == 'POST':
        if len(cart_list)<8 :
            cart_list.append(request.form['name'])
            flg=False
        else:
            print('over')
            flg = True

    if len(cart_list) == 0:
        is_zero = True
    else:
        is_zero = False
    
    session['cart_items'] = cart_list

    return render_template('product.html', params=cart_list,is_upper=flg,is_zero = is_zero)

@app.route('/product/<id>',methods=['GET'])
def product_delete(id):
    cart_list = session['cart_items']
    cart_list.pop(int(id))
    session['cart_items'] = cart_list
    return redirect(url_for('product_detail'))


@app.route('/product/confirm', methods=['GET'])
def product_confirm():
    cart_list = session['cart_items']

    return render_template('product_confirm.html', params=cart_list,cart_len=len(cart_list))


@app.route('/product/thanks',methods=['GET'])
def product_thanks():
    cart_list = session['cart_items']

    return render_template('product_thanks.html',params=cart_list)




@app.route('/product/delete_all')
def product_delete_all():
    session['cart_items'] = []

    return redirect(url_for('product_detail'))

@app.route("/car/cx-3")
def car_cx3():

    return render_template("product.html")


@app.route("/car/mazda2")
def car_mazda2():

    return render_template("product.html")

@app.route("/cars")
def cars():
    car_names = ['mazda2', 'mazda3-fastback', 'mazda3-sedan', 'mazda6-sedan', 'mazda6-wagon', 'cx-3', 'cx-30', 'cx-5', 'cx-8', 'roadster', 'roadsterrf']
    return render_template('cars.html', params=car_names)


@app.route("/cars/<car_name>")
def car_detail(car_name):
    title = car_name
    if 'current_car_name' not in session:
        session['current_car_name'] = ''
    session['current_car_name'] = car_name
    current_car_name = session['current_car_name']
    return render_template('car_detail.html', car_name=car_name)

@app.route("/purchase/estimate")
def estimate(methods=['GET']):
    if 'current_car_name' not in session:
        return redirect(url_for('cars'))
    current_car_name = session['current_car_name']
    return render_template('estimate.html', current_car_name=current_car_name)

@app.route("/purchase/catalog")
def catalog():
    if 'current_car_name' not in session:
        return redirect(url_for('cars'))
    current_car_name = session['current_car_name']
    return render_template('catalog_input.html', current_car_name=current_car_name)

@app.route("/purchase/catalog/confirm", methods=['POST'])
def catalog_confirm():
    current_car_name = session['current_car_name']
    params = {}
    if request.method == 'POST':
        params = request.form
    return render_template('catalog_confirm.html', params=params, current_car_name=current_car_name)

@app.route('/purchase/catalog/thanks',methods=['POST'])
def catalog_thanks():
    return render_template('catalog_thanks.html')

if __name__ == '__main__':
    app.debug = True
    app.run()


