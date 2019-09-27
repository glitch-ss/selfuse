#-*- coding:utf-8

from bs4 import BeautifulSoup
import requests
import random



class ippool():
    def __init__(self):
        self.headers = {
            'Accept':'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'ip.ihuan.me',
            'Referer':'https://ip.ihuan.me',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/69.0'
        }
        self.ip_list = []
        self.page_list = []
        self.s = requests.Session()
        self.url = 'https://ip.ihuan.me/address/576O5Zu9.html'

    def get_soup(self):
        self.response = self.s.get(self.url, headers=self.headers)
        if self.response.status_code != 200:
            return False
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    def get_ip_list(self, soup):
        tbody = soup.find_all('tbody')[0]
        tr_list = tbody.find_all('tr')
        for tr in tr_list:
            td_list = tr.find_all('td')
            ip = td_list[0].get_text()
            port = td_list[1].get_text()
            https = td_list[4].get_text()
            if https.strip() == u'支持':
                self.ip_list.append(ip+':'+port)

    def get_page(self, soup):
        pagination = soup.find_all('ul', attrs={'class':'pagination'})[0]
        page_a_list = pagination.find_all('a')
        for a in page_a_list:
            self.page_list.append(a['href'])

    def update_url(self):
        page = self.page_list.pop()
        if page == 1:
            return
        self.url = 'https://ip.ihuan.me/address/576O5Zu9.html' + page

    def process(self):
        self.get_soup()
        self.get_page(self.soup)
        for page in self.page_list:
            self.update_url()
            self.get_soup()
            self.get_ip_list(self.soup)
        return self.ip_list

    def get_one(self):
        count = len(self.ip_list)
        return self.ip_list[random.randint(0,count)]

