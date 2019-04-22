#-*- coding:utf-8

from app import app
from flask import json, jsonify,request,render_template
from app.process.express import Express
import hashlib

#from app import do_sql

#s=do_sql.do_sql()
@app.route('/')
@app.route('/index')
def index():
    return render_template("Hello World")

@app.route('/express')
def express():
    name_list=[]       
    a=Express('13162580787','atobefuji')
    list = a.get_history_list('4-22')
    for i in list:
        b = a.get_info(i)
        name_list.append(b)
    return render_template('express.html', name_list=name_list)

@app.route('/getlist', methods=['POST'])
def form_data():
    print "#####"
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    print type(json_data)
    return jsonify({'status': '0', 'errmsg': u'登录成功！'})

@app.route('/wx', methods=['GET', 'POST'])
def wx():
    print '$#1'
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    token='luodanting'
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    print "handle/GET func: hashcode, signature: ", hashcode, signature
    if hashcode == signature:
        return echostr
    else:
        return ""
    
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