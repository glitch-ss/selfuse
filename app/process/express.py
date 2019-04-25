#-*- coding:utf-8
import requests
import re
import chardet
from bs4 import BeautifulSoup
import os
import json

class Express():
    login_page='https://m.kuaidihelp.com/account/login'
    def __init__(self,name=None,password=None):
        self.name=name
        self.password=password
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
        item_list=[]
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
        result = json.loads(response.text)['data']['list']
        for item in result:
            if date in item['date']:
                item_list.append(item['id'])
        return item_list
    
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
        temp = soup.find_all('span',attrs={'id':'contents'})
        res.append(temp[0].get_text())
        name = soup.find_all('div',attrs={'class':'css-table-common'})[1]
        a=name.find_all('span',attrs={'class':'w-11'})
        res.append(a[0].get_text().split('1')[0].strip())
        return res

        