#-*- coding:utf-8

from app import app
from flask import json, jsonify,request,render_template
from app.process.express import Express
import hashlib
import exceptions

#from app import do_sql

#s=do_sql.do_sql()
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/express', methods=['GET','POST'])
def express(): 
    name_list=[]
    date=""
    try:
        date =  request.args.get('date')
    except:
        print 'erro'    
    #key='05-12'
    if date is not None and "-" in date:
        print 'e'
        a=Express('13162580787','atobefuji')
        list = a.get_history_list(date)
        print len(list)
        for i in list:
            b = a.get_info(i)
            name_list.append(b)
    return render_template('express.html', name_list=name_list)

@app.route('/innerexpress', methods=['POST'])
def innerexpress():
    name_list=[]
    date=""
    try:
        date = request.form.get('date')
        print date
    except Exception, e:
        print e
        pass    
    #key='05-12'
    print type(date)
    if date is not None and "-" in date:
        a=Express('13162580787','atobefuji')
        list = a.get_history_list(date)
        print len(list)
        for i in list:
            b = a.get_info(i)
            name_list.append(b)
    print len(name_list)
    return jsonify({'name_list':name_list})

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