#-*- coding:utf-8
from app import app
from flask import json, jsonify,request
from app import do_sql

s=do_sql.do_sql()
@app.route('/')
@app.route('/index')
def index():
    return "Hello World"

@app.route('/getlist', methods=['POST'])
def form_data():
    print "#####"
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    print type(json_data)
    return jsonify({'status': '0', 'errmsg': u'登录成功！'})

@app.route('/wx', methods=['GET', 'POST'])
def wx():
    print '$#'
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    print type(data)
    print data
    return jsonify({'status': '0', 'errmsg': u'登录成功！'})
    
@app.route('/additem',methods=['POST'])
def add_data():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if id in json_data:
        id = json_data['id']
    else:
        return jsonify({'status': '-1', 'errmsg': u'id not set, wrong set'})
    number = json_data['number']
    name = json_data['name']
    price = json_data['price']
    status = json_data['status']
    description =json_data['description']
    s.add_item(id, name, number, price, status, description)