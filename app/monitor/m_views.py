from app import app
from flask import json, jsonify, request, render_template
from app.monitor.sephora import *
from app.monitor.sephora import pSephora, sephora_list
from app.monitor.Nordstrom import pNordstrom, nordstrom_list
from app.monitor.macys import pMacys, macys_list
from app.monitor.Est import pEst, est_list
import time
from threading import Thread
from werkzeug.utils import secure_filename
import exceptions
import mysql.connector

sephora_name_list = {}
nordstrom_name_list = {}
macys_name_list = {}

conn = mysql.connector.connect(host='localhost', user='root',
                       passwd='atobefuji', port=3306, db='stock')
cursor = conn.cursor()


def config_output(list_dict):
    output = []
    count = 0
    for i in list_dict.keys():
        now = count / 10
        if count % 10 == 0:
            output.append({})
        output[now][i] = list_dict[i]
        count += 1
    print output
    return output


class myThread(Thread):
    def __init__(self, fun):
        Thread.__init__(self)
        self.fun = fun

    def run(self):
        print "Starting"
        self.fun.process()
        print "Exiting"


@app.route('/sephora', methods=['GET', 'POST'])
def Sephora():
    global sephora_list
    if request.method == 'POST':
        action = request.form.get('action')
        band = request.form.get('band')
        ID = request.form.get('item_id')
        color = request.form.get('color')
        if action != 'del':
            if band == "sephora":
                if ID in sephora_list.keys():
                    return jsonify({'sephora_list': sephora_list, 'error_message': "ID existed"})
                s = pSephora(ID)
            elif band == "nordstrom":
                if ID in nordstrom_list.keys():
                    return jsonify({'nordstrom_list': nordstrom_list, 'error_message': "ID existed"})
                s = pNordstrom(ID, color)
            elif band == "macys":
                if ID in macys_list.keys():
                    return jsonify({'macys_list': macys_list, 'error_message': "ID existed"})
                s = pMacys(ID, color)
            elif band == "esteelaud":
                if ID in est_list.keys():
                    return jsonify({'est_list': est_list, 'error_message': "ID existed"})
                s = pEst(ID)
            else:
                return render_template('Sephora.html', sephora_list=config_output(sephora_list))
            t = myThread(s)
            t.start()
            return jsonify({'sephora_list': config_output(sephora_list), 'nordstrom_list': config_output(nordstrom_list), 'macys_list': config_output(macys_list), 'est_list': config_output(est_list)})
        else:
            if ID in sephora_list.keys():
                print ID
                del sephora_list[ID]
            elif ID in nordstrom_list.keys():
                del nordstrom_list[ID]
            elif ID in macys_list.keys():
                del macys_list[ID]
            elif ID in est_list.keys():
                del est_list[ID]
            return jsonify({'status': 'success'})
    else:
        return render_template('sephora.html', sephora_list=config_output(sephora_list), nordstrom_list=config_output(nordstrom_list), macys_list=config_output(macys_list), est_list=config_output(est_list))


@app.route('/namelist', methods=['GET', 'POST'])
def name_list():
    return render_template('name_list.html', sephora_name_list=config_output(sephora_name_list), nordstrom_name_list=config_output(nordstrom_name_list), macys_list=config_output(macys_list), est_list=config_output(est_list))


@app.template_filter('get_mod')
def get_mod(a, b=2):
    return int(a) % int(b)


@app.route('/update_key', methods=['GET', 'POST'])
def update_key():
    if request.method == 'POST':
        item_id = request.form.get('id')
        url = request.form.get('url')
        band = request.form.get('band')
        name = request.form.get('name')


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('files')
        file_name = secure_filename(f.filename)
        band = file_name.split('.')[0]
        if band == 'Sephora':
            print 'test'
            for l in f.readlines():
                l = l.strip()
                if l in sephora_list.keys():
                    print "{0} is in list, so continue".format(l)
                    continue
                s = pSephora(l)
                t = myThread(s)
                t.start()
            return jsonify({'sephora_list': config_output(sephora_list)})
        elif band == 'Nordstrom':
            color = None
            for l in f.readlines():
                l = l.split(',')
                now_item = l[0]
                if len(l) > 1:
                    color = l[1].strip()
                s = pNordstrom(now_item, color)
                t = myThread(s)
                t.start()
            return jsonify({'status': 'fail'})
        elif band == 'Macys':
            color = None
            for l in f.readlines():
                l = l.split(',')
                now_item = l[0]
                if len(l) > 1:
                    color = l[1].strip()
                s = pMacys(now_item, color)
                t = myThread(s)
                t.start()
            return jsonify({'status': 'fail'})
        elif band == 'Esteelaud':
            for l in f.readlines():
                l = l.strip()
                s = pEst(l)
                t = myThread(s)
                t.start()
            return jsonify({'est_list': config_output(est_list)})


@app.route('/key_list', methods=['GET', 'POST'])
def key_list():
    if request.method == 'POST':
        band = request.form.get('band')
        query_cmd = "select id, name, color from {0};".format(band)
        result = cursor.execute(query_cmd)
        print result
        return jsonify({'key_list': result})