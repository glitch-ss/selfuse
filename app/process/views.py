# -*- coding:utf-8 -*-

from app import app
from flask import json, jsonify, request, render_template
from app.process.express import Express
from app.process.mk import *
from bs4 import UnicodeDammit
import hashlib
import time
import threading
import exceptions
price_dict = {
    u'北京市': 8,
    u'上海市': 6,
    u'江苏省': 6,
    u'安徽省': 6,
    u'浙江省': 6,
    u'山东省': 8,
    u'广东省': 8,
    u'福建省': 8,
    u'湖南省': 8,
    u'湖北省': 8,
    u'江西省': 8,
    u'天津市': 8,
    u'河南省': 8,
    u'河北省': 8,
    u'山西省': 8,
    u'四川省': 8,
    u'陕西省': 8,
    u'海南省': 8,
    u'重庆市': 8,
    u'辽宁省': 8,
    u'吉林省': 8,
    u'云南省': 8,
    u'广西壮族自治区': 8,
    u'宁夏回族自治区': 8,
    u'贵州省': 8,
    u'黑龙江省': 8,
    u'宁夏省': 10,
    u'青海省': 10,
    u'甘肃省': 10,
    u'内蒙古自治区': 10,
    u'新疆维吾尔自治区': 10,
    u'西藏自治区': 10,
}
stop_id = []
inspect_sephora_list = {}
inspect_mk_list = {}
#from app import do_sql


def inspect_mk_by_url(url):
    a = MK(url)
    status = a.get_stock_status()
    inspect_mk_list[status[0]] = status[1]
    while status[1] == "Out of Stock" and status[0] not in stop_id:
        time.sleep(180)
        status = a.get_stock_status()
    inspect_mk_list[status[0]] = status[1]
    if status[1] == 'In Stock':
        lucien801('MK', status[0] + ': is in stock')
    inspect_mk_list.pop(status[1])

# s=do_sql.do_sql()


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
    print "####" + str(stop_id)
    return jsonify({'status': 'success'})


@app.route('/express', methods=['GET', 'POST'])
def express():
    name_list = []
    date = ""
    try:
        date = request.args.get('date')
    except:
        print 'erro'
    # key='05-12'
    if date is not None and "-" in date:
        print 'e'
        a = Express('13162580787', 'atobefuji')
        list = a.get_history_list(date)
        print len(list)
        for i in list:
            b = a.get_info(i)
            name_list.append(b)
    return render_template('express.html', name_list=name_list)


@app.route('/mk', methods=['GET', 'POST'])
def mk():
    method = request.method
    if method == 'GET':
        return render_template('mk.html', inspect_list=inspect_mk_list)
    elif method == 'POST':
        url = request.form.get('url')
        name = url.split('com/')[1].split('/_')[0].replace('-', ' ')
        if name not in inspect_mk_list:
            t = threading.Thread(target=inspect_mk_by_url, args=(url,))
            t.start()
        time.sleep(3)
        return jsonify({'inspect_list': inspect_sephora_list})


@app.route('/innerexpress', methods=['POST'])
def innerexpress():
    name_list = []
    price = 0
    date = ""
    try:
        date = request.form.get('date')
        print date
    except Exception, e:
        print e
        pass
    # key='05-12'
    print type(date)
    if date is not None and "-" in date:
        a = Express('13162580787', 'atobefuji')
        list = a.get_history_list(date)
        print len(list)
        for i in list:
            b = a.get_info(i)
            name_list.append(b)
    print len(name_list)
    price_list = a.province_list
    for a in price_list:
        print a.encode('gbk')
        price += price_dict[a]
    return jsonify({'name_list': name_list, 'price': price})


@app.route('/wx', methods=['GET', 'POST'])
def wx():
    print '$#1'
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    token = 'luodanting'
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
