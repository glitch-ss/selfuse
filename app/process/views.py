# -*- coding:utf-8 -*-

from app import app
from flask import json, jsonify, request, render_template
from app.process.express import Express, price_dict
from app.process.mk import *
from bs4 import UnicodeDammit
from datetime import datetime
import pandas as pd
import os
import hashlib
import time
import threading
import exceptions
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
        file_path = 'app/static/file/excel/' + date
        if os.path.exists(file_path):
            print os.path.exists(file_path)
            df = pd.read_excel(file_path)
            for item in df.values:
                item.remove(item[0])
                name_list.append(item)
        else:
            print 'ssss'
            a = Express('13162580787', 'atobefuji')
            lists = a.get_history_list(date)
            print len(lists)
            for i in lists:
                b = a.get_info(i)
                name_list.append(b)
            print 'generate'
            a.generate_file(date, name_list)
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
        mon = date.split('-')[0]
        day = date.split('-')[1]
        now_year = str(datetime.now().year)
        file_path = 'app/static/file/excel/' + now_year
        if not os.path.exists(file_path):
            print 'create menu'
            os.makedirs(file_path)
        file_path = file_path + '/' + mon
        if not os.path.exists(file_path):
            print 'create menu'
            os.makedirs(file_path)
        file_path = file_path + '/' + day
        if os.path.exists(file_path):
            print os.path.exists(file_path)
            df = pd.read_excel(file_path)
            for item in df.values:
                item = list(item)
                item.remove(item[0])
                name_list.append(item)
        else:
            a = Express('13162580787', 'atobefuji')
            lists = a.get_history_list(date)
            print len(lists)
            for i in lists:
                b = a.get_info(i)
                name_list.append(b)
            if len(lists) > 0:
                a.generate_file(date, name_list)
    print len(name_list)
    for a in name_list:
        # print a.encode('gbk')
        print a
        price += int(a[5])
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


@app.route('/cz', methods=['GET', 'POST'])
def cz():
    method = request.method
    if method == 'POST':
        page = request.form.get('page')
        if page == 'market':
            return jsonify({'market_list': [['1', 'iso1', '第一个iso，请轻一点'], ['2', 'iso2', '第二个iso， 随便草']]})
        elif page == 'doc':
            return jsonify({'doc': {'1': ['呵呵哒', '/static/file/video/test.MOV'],
                                    '2': ['我是警察', '/static/file/video/test.MOV']}})
        elif page == 'myrpa':
            return jsonify({'myrpa': {'1': {'name': 'iso1', 'instance': [['0', '实例名1', '3天', 'http://www.baidu.com'], ['1', '实例名2', '已到期']]},
                                      '2': {'name': 'iso2', 'instance': [['3', '实例名1', '5天', 'http://   www.baidu.com'], ['1', '实例名2', '6天']]}}})
    print "cz"
    return render_template("self.html")
