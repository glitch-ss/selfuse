#-*- coding:utf-8
import requests
import re   
import chardet
from bs4 import BeautifulSoup
import os
import json
import logging
import time
import datetime
from mail import lucien801
'''
logger=logging.getLogger('TEST')
logger.setLevel(logging.INFO)
fh = logging.FileHandler("./app/static/log/test.log")
formatter=logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
'''
global my_proxy  
global est_list
global lmail
est_list = {}
#lmail = lucien801()
my_proxy=None

class Est():
    def __init__(self, url=None):
        self.url = url
        self.product_id = None
        self.type_id = None
        self.name = None
        self.normal_headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Host':'www.esteelauder.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Cache-Control':'max-age=0',
            }
        self.post_headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'Cache-Control':'max-age=0',
            'Host':'www.esteelauder.com',
            'Origin':'https://www.esteelauder.com',
            'Refer':url,
            'Connection':'keep-alive',
            'Content-Length':'98',
            'X-Requested-With':'XMLHttpRequest',
            }
        self.get_id()
        print 'init {0}'.format(self.product_id)
        self.post_data = {"method": "prodcat.querykey",
                        "products":["PROD{0}".format(self.product_id)],
                        "query_key": "catalog-mpp-volatile",
                        "id":1}
        print self.url

    def get_status(self):
        response = requests.post("https://www.esteelauder.com/rpc/jsonrpc.tmpl", data=self.post_data, headers=self.post_headers)
        if response.status_code == 200:
            result = json.loads(response.text)[0]
        else:
            print response.status_code
            return False
        try:
            if self.name is None:
                self.name = result['result']['data']['dataLayer']['product_impression_name'][0]
            status = result['result']['value']['products'][0]['isShoppable']
        except Exception, e:
            print 'get name fail, get status fail'
            print e
            return False
        return status

    def get_id(self):
        try:
            temp_url = self.url.split('product/')[1]
            temp_id = re.findall('\d*\/\d*', temp_url)[0].split('/')
            self.product_id = temp_id[1]
            self.type_id = temp_id[0]
            
        except Exception, e:
            print e
            return None

class pEst(Est):
    def __init__(self, url):
        self.show_status = ['N/A', 'BUY']
        Est.__init__(self, url)
        self.ID = self.product_id
        if self.ID in est_list:
            self.duplicate = True
        else:
            self.duplicate = False
        self.status = self.get_status()
        self.info = [self.ID, self.name, self.url, str(self.show_status[self.status])]
        print self.info
        #logger.info('Macys {0} the status is {1}'.format(self.ID, self.status))
        est_list[self.ID] = self.info

    def process(self):
        global est_list
        global lmail
        count = 0
        if self.duplicate:
            return
        print 'start suspect {0}'.format(self.ID)
        while self.ID in est_list:
            if count == 100:
                count = 0
                print "esteelauder {0} is ongoing".format(self.ID)
            count += 1
            time.sleep(5)
            try:
                status = self.get_status()
                if status != self.status:
                    self.status = status
                    est_list[self.ID] = self.info
                    logging.info('esteelauder {0} {1} the status change to {2}'.format(self.name, self.status))
                    if status == 1:
                        m = '{2} esteelauder {0} {1} the status change to available \n {3}'.format(self.name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.url)
                        lmail.sm('esteelauder', m)
                self.info[3]=str(self.show_status[status])
            except Exception, e:
                print self.ID
                print e


#a=Est('https://www.esteelauder.com/product/681/46655/product-catalog/skincare/advanced-night-repair-eye-concentrate-matrix/synchronized-recovery')
#print type(a.get_status())