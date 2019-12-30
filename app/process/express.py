#-*- coding:utf-8
import requests
import re
import chardet
from bs4 import BeautifulSoup
import os
import json
import pandas as pd
from datetime import datetime
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

class Express():
    login_page='https://m.kuaidihelp.com/account/login'
    def __init__(self,name=None,password=None):
        self.name=name
        self.password=password
        self.province_list=[]
        self.post_headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept':'application/json, text/plain, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'Host':'m.kuaidihelp.com',
            'Refer':'https://m.kuaidihelp.com/index/login?to=/members/index',
            'X-Requested-With':'XMLHttpRequest',
            'TE':'Trailers',
            'Connection':'keep-alive',
            'Content-Length':'52',
            }
        if self.name is not None:
            self.data={'name':'13162580787', 'pwd':'atobefuji', 'to':'/members/index'}
            self.s=requests.Session()
            response = self.s.post('https://m.kuaidihelp.com/account/login', self.data, headers = self.post_headers)
            print response.text
    
    def get_history_list(self,date):
        target_mon = date.split('-')[0]
        target_day = date.split('-')[1]
        if date=="":
            return []
        self.item_list={}
        province_list=[]
        self.s.headers['Content-Length']='29'
        self.s.headers['X-Requested-With']='XMLHTTPRequest'
        self.s.headers['Refer']='https://m.kuaidihelp.com/order/openHistory'
        self.s.headers['Host']='m.kuaidihelp.com'
        self.s.headers['Accept']='application/json, text/javascript, */*; q=0.01'
        self.s.headers['date']='Mon, 22 Apr 2019 13:10:39 GMT'
        self.s.headers['Cache-Control']='max-age=0'
        self.s.headers['user-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
        data={'action':'history'}
        response = self.s.post('https://m.kuaidihelp.com/order/ajax', data=data, allow_redirects = False)
        self.result = json.loads(response.text)['data']['list']
        self.province_list=[]
        for item in self.result:
            if date in item['date']:
                if item['status'] == 1:
                    continue
                self.item_list[item['id']] = item['shipping_province']
                self.province_list.append(item['shipping_province'])
        count = 2
        status = True
        while status:
            data= {'action': 'history','page': count}
            try:
                print count
                response = self.s.post('https://m.kuaidihelp.com/order/ajax', data=data, allow_redirects = False)
                self.result2 = json.loads(response.text)['data']['list']
                self.result = self.result + self.result2
                for item in self.result2:
                    if item['status'] == 1:
                        continue
                    item_date = item['date'].split(' ')[0].split('-')
                    print item_date[0] + '-'+item_date[1]
                    print date
                    if int(item_date[0]) > int(target_mon):
                        status = True
                    elif int(item_date[1]) >= int(target_day) and int(item_date[0]) == int(target_mon):
                        status = True
                    else:
                        status = False
                    print status
                    if date in item['date'] and item not in self.item_list.keys():
                        self.item_list[item['id']] = item['shipping_province']
                        self.province_list.append(item['shipping_province'])
            except Exception, e:
                print e
            count += 1
        return self.item_list.keys()
    
    def get_info(self,id,t=None):
        res=[]
        url = 'https://m.kuaidihelp.com/order/detail?id='+id
        self.s.headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        if 'date' in self.s.headers:
            self.s.headers.pop('date')
            self.s.headers.pop('X-Requested-With')
            self.s.headers.pop('Content-Length')
            
        response = self.s.get(url, allow_redirects = False )
        soup=BeautifulSoup(response.text,'html.parser')
        temp_number = soup.find_all('span',attrs={'id':'contents'})
        res.append(temp_number[0].get_text())
        name = soup.find_all('div',attrs={'class':'css-table-common'})[1]
        weight = soup.find_all('div', attrs={'class':'css-waybill-info'})[0]
        weight_soup = weight.nextSibling.nextSibling.nextSibling.nextSibling
        t = weight_soup.contents[3].find_all('div', attrs={'class':'mt-0_5'})[0].get_text()
        weight = t.split(u'公斤')[0]
        name_soup = name.find_all('span',attrs={'class':'w-11'})
        phone_num = name_soup[0].find_all('em')[0].get_text()
        res.append(name_soup[0].get_text().split('1')[0].strip())
        res.append(weight)
        res.append(phone_num)
        province = self.item_list[id]
        res.append(province)
        res.append(price_dict[province])
        return res

    def generate_file(self, date, data):
        path = 'app/static/file/excel/' + str(datetime.now().year)
        file = os.listdir(path)
        print file
        if date not in file:
            file = pd.DataFrame(data)
            file.to_excel(path+'/'+ date.split('-')[0] + '/' + date.split('-')[1], engine='openpyxl')