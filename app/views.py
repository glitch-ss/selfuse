#-*- coding:utf-8

from app import app
from flask import json, jsonify,request,render_template
from app.process.express import Express
from app.process.mail import *
from app.process.sephora import *
from app.process.mk import *
import hashlib
import time
import threading
import exceptions
price_dict={
    '北京市':8,
    '上海市':6,
    '江苏省':6,
    '安徽省':6,
    '浙江省':6,
    '山东省':8,
    '广东省':8,
    '福建省':8,
    '湖南省':8,
    '湖北省':8,
    '江西省':8,
    '天津市':8,
    '河南省':8,
    '河北省':8,
    '山西省':8,
    '四川省':8,
    '陕西省':8,
    '海南省':8,
    '重庆市':8,
    '辽宁省':8,
    '吉林省':8,
    '云南省':8,
    '广西省':8,
    '贵州省':8,
    '黑龙江省':8,
    '宁夏省':10,
    '青海省':10,
    '甘肃省':10,
    '内蒙古省':10,
    '新疆省':10,
    '西藏省':10,
}
stop_id=[]
inspect_sephora_list={}
inspect_mk_list={}
#from app import do_sql
def inspect_sephora_by_id(id):
    a=Sephore()
    status = a.get_item_status_by_id(id)
    inspect_sephora_list[id]=status
    print stop_id
    while status[0]=='inactive' and id not in stop_id:
        time.sleep(180)
        status = a.get_item_status_by_id(id)
    inspect_sephora_list[id]=status
    if status[0]!='inactive':
        lucien801('Sephora', id + ': ' + status[1] + ' is in stock')
    inspect_sephora_list.pop(id)
    
def inspect_mk_by_url(url):
    a=MK(url)
    status = a.get_stock_status()
    inspect_mk_list[status[0]]=status[1]
    while status[1]=="Out of Stock" and status[0] not in stop_id:
        time.sleep(180)
        status = a.get_stock_status()
    inspect_mk_list[status[0]]=status[1]
    if status[1]=='In Stock':
        lucien801('MK', status[0] + ': is in stock')
    inspect_mk_list.pop(status[1])

#s=do_sql.do_sql()
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/stop', methods=['POST'])
def set_stop():
    key = request.form.get('key')
    for i in stop_id:
        if i not in inspect_sephora_list and i not in inspect_mk_list:
            stop_id.remove(i)
    stop_id.append(key)
    print "####"+str(stop_id)
    return jsonify({'status': 'success'})

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

@app.route('/sephora', methods=['GET','POST'])
def sephora():
    method = request.method
    if method=='GET':
        print inspect_sephora_list
        return render_template('sephora.html', inspect_list=inspect_sephora_list)
    elif method=='POST':
        id = request.form.get('id')
        if id not in inspect_sephora_list:
            t = threading.Thread(target=inspect_sephora_by_id, args=(id,))
            t.start()
        time.sleep(3)
        print inspect_sephora_list
        return jsonify({'inspect_list': inspect_sephora_list})
    
@app.route('/mk', methods=['GET','POST'])
def mk():
    method = request.method
    if method=='GET':
        return render_template('mk.html', inspect_list=inspect_mk_list)
    elif method=='POST':
        url = request.form.get('url')
        name=url.split('com/')[1].split('/_')[0].replace('-', ' ')
        if name not in inspect_mk_list:
            t=threading.Thread(target=inspect_mk_by_url, args=(url,))
            t.start()
        time.sleep(3)
        return jsonify({'inspect_list': inspect_sephora_list})

@app.route('/innerexpress', methods=['POST'])
def innerexpress():
    name_list=[]
    price=0
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
    price_list = a.province_list
    for a in price_list:
        price += price_dict[a]
    return jsonify({'name_list':name_list, 'price':price})

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