# -*- encoding:utf-8 -*-
from Browser import *
import re
import chardet

Path=os.path.abspath('.')

old_socket=urllib2.socket.socket
'''
proxy_srv='cn-proxy.jp.oracle.com'
proxy_port=80
socks.setdefaultproxy(socks.PROXY_TYPE_HTTP,proxy_srv,proxy_port)
socks.wrapmodule(urllib2)
'''

#r=redis.Redis(host='127.0.0.1', port=6379, db=0)
r=None

ks=ks_Browser()
ks_dict=ks.get_category_soup()
print 'get category soup done'
#urllib2.socket.socket=old_socket
category_urls=ks.get_bag_urls(ks_dict,r)
#socks.wrapmodule(urllib2)
state=1

for key in category_urls:
    if key!='handbags':
        continue
    print 'start handbags'
    Path_temp=os.path.join(Path,key)
    if not os.path.exists(str(Path_temp)):
        os.mkdir(str(Path_temp))
    for url in category_urls[key]:
        print 'get bag soup'
        soup=ks.get_page_soup(url)
        while soup=="False":
            print 'get soup fail, try again'
            soup=ks.get_page_soup(url)

        print 'get bag name'
        ks.name=ks.get_bag_name(soup,url)
        '''if 'street brennan' in ks.name:
            state=1
            continue'''
        temp=ks.name.encode('utf-8')
        if state == 0:
            continue
        ks.name=str(ks.name).replace('/','_')
        filename=os.path.join(Path_temp,ks.name)
        if os.path.exists(str(filename)):
            pass
        else:
            os.mkdir(str(filename))
            print "make dir %s"%(str(filename))
        if not ks.get_bag_details(soup,Path_temp):
            print ks.name
            continue

        print 'get color url'
        color_url=ks.get_color_page(soup)
        for url in color_url:
            print 'get color page'
            soup=ks.get_page_soup(url, 'POST')
            while soup=="False" or isinstance(soup,str) or soup==None or len(soup.find_all('ul',attrs={'class':'swatches'}))==0:
                print 'color page cannot be opened'
                print url
                soup=ks.get_page_soup(url, 'POST')
            img_urls=ks.get_img_url(soup)                
            ks.color=ks.get_bag_color(soup)
            ks.color=str(ks.color).replace('/','_')
            color_url=ks.get_color_img(soup)            
            i=1
            
            for i_urls in img_urls:
                ks.img_download(i_urls,i,Path_temp)
                i+=1
            for key in color_url:
                if color_url[key]==None:
                    break
                ks.img_download(color_url[key],10,Path_temp,key)


