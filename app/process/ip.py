# -*- coding:utf-8

from bs4 import BeautifulSoup
import requests
import random


def get_ip_list(url):
    session = requests.Session()
    session.headers = headers
    ip_list = []
    new_list = []
    for i in range(1, 8):
        web_data = session.get(url + str(i))
        soup = BeautifulSoup(web_data.text, 'html.parser')
        ips = soup.find_all('tr')
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
    # 检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
    for ip in ip_list:
        try:
            proxy_host = "https://" + ip
            proxy_temp = {"https": "https://" + ip, "http":"http://" + ip}
            new_list.append(proxy_temp)
            print 1
            res = urllib.urlopen(url, proxies=proxy_temp).read()
            print 2
        except Exception as e:
            ip_list.remove(ip)
            continue
    # print ip_list
    return new_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def getHTMLText(url, proxies, headers):

    r = requests.get(url, headers=headers, proxies=proxies)
    return r


if __name__ == '__main__':
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               #'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'www.xicidaili.com',
               #'Sec-Fetch-Mode': 'navigate',
               #'Sec-Fetch-Site': 'none',
               #'Sec-Fetch-User': '?1',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
    url = 'https://www.xicidaili.com/nn/'
    new_list = get_ip_list(url)
    print len(new_list)
    # proxies = get_random_ip(ip_list)
    # print(proxies)
    '''proxies = {
        "http": "122.193.246.104:9999",
        "https": "163.204.241.35:9999",
    }'''
    headers = {'Accept': 'text/css,*/*;q=0.1',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Connection': 'keep-alive',
               'Host': 'luolii55luolii55luolii55luolii…olii5luolii55.loliloli555.top',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; r…) Gecko/20100101 Firefox/68.0'}
    u = "http://luolii55luolii55luolii55luolii55luolii5luolii55.loliloli555.top/portal.php?x=680309"
    for proxies in new_list:
    	print proxies
    	try:
            print getHTMLText(u, proxies, headers)
        except:
        	pass
