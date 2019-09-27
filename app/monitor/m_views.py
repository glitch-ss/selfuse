from app import app
from flask import json, jsonify, request, render_template
from app.monitor.sephora import *
from app.monitor.sephora import pSephora, sephora_list
from app.monitor.Nordstrom import pNordstrom, nordstrom_list
from app.monitro.ippool import ippool
import time
from threading import Thread
from werkzeug.utils import secure_filename
import exceptions

sephora_name_list={}
nordstrom_name_list={}
ip_p = ippool()
ip_p.process()
my_proxy = ip_p.get_one()

def config_output(list_dict):
    output = []
    count = 0
    for i in list_dict.keys():
        now = count / 10
        if count % 10 == 0:
            output.append({})
        output[now][i] = list_dict[i]
        count += 1
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
            else:
                return render_template('Sephora.html', sephora_list=config_output(sephora_list))
            t = myThread(s)
            t.start()
            return jsonify({'sephora_list': config_output(sephora_list), 'nordstrom_list':config_output(nordstrom_list)})
        else:
            if ID in sephora_list.keys():
                print ID
                del sephora_list[ID]
            elif ID in nordstrom_list.keys():
                nordstrom_list.remove(ID)
            return jsonify({'status': 'success'})
    else:
        return render_template('sephora.html', sephora_list=config_output(sephora_list), nordstrom_list=config_output(nordstrom_list))

@app.route('/namelist', methods=['GET', 'POST'])
def name_list():
	return render_template('name_list.html', sephora_name_list=config_output(sephora_name_list), nordstrom_name_list=config_output(nordstrom_name_list))

@app.template_filter('get_mod')
def get_mod(a, b=2):
    return int(a) % int(b)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('files')
        file_name = secure_filename(f.filename)
        band = file_name.split('.')[0]
        if band == 'Sephora':
            for l in f.readlines():
                l = l.strip()
                if l in sephora_list.keys():
                    print "{0} is in list, so continue".format(l)
                    continue
                s = pSephora(l)
                t = myThread(s)
                t.start()
            return jsonify({'sephora_list': config_output(sephora_list), 'error_message': "ID existed"})
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
