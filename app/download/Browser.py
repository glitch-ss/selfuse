import urllib2
import urllib
import cookielib
import re
import socks
print 'before'
from bs4 import BeautifulSoup
print 'after'
import imghdr
import os
import requests

class Browser():
    login_page=None
    def __init__(self,user=None,password=None):
        self.name=None
        self.color=None
        self.user=user
        self.password=password
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}

        if user is not None:
            try:
                cj=cookielib.CookieJar()
                self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                self.opener.addheaders=[('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')]
                self.data=urllib.urlencode({"email":self.user,"password":self.password})
                test=self.opener.open(self.login_page,self.data)
                #print test.read()

            except Exception,e:
                print str(e)
        else:
            try:
                cj = cookielib.CookieJar()
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                self.opener.addheaders = [('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')]
                self.s = requests

            except Exception,e:
                print str(e)
 
    def get_page_soup(self, url, way='GET'):
        try:
            if way == 'GET':
                response = self.s.get(url, headers=self.headers)
            elif way == 'POST':
                response = self.s.post(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,'html.parser')
                return soup
            else:
                print response.status_code
                print response.text
                return None
        except Exception, e:
            print str(e)
            print url
            return "False"

    def get_img_url(self,soup):
        pass

    def get_bag_name(self,soup):
        pass

    def get_bag_color(self,soup):
        pass

    def get_color_page(self,soup):
        return None

    def img_download(self,url,i,Path,col_name=None):
        self.opener.addheaders=[('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')]
        picture = self.get_img_content(url)
        imgType=imghdr.what("",picture)
        if imgType==None:
            imgType="jpeg"
        if col_name is not None:
            color_name=self.name+'_'+col_name
        else:
            color_name=self.name+'_'+self.color
        if i==10:
            filename=str(color_name)+"+"+str(i)+"."+str(imgType)
        filename=str(color_name)+"+"+str(i)+"."+str(imgType)
        path=Path+'\\'+self.name+'\\'
        jpg=path+filename
        print jpg
        f=open(jpg,'wb')
        f.write(picture)
        f.close()
        self.opener.addheaders=[('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')]

    def get_img_content(self,url):
        state=0
        try:
            page=self.opener.open(url)
        except Exception,e:
            result=str(e)
            print result
            print url
            state=1
            if '403' in result:
                state=2
        if state==2:
            return 0
        while state==1:
            try:
                page=self.opener.open(url)
                state=0
            except Exception,e:
                state=1
        picture=page.read()
        return picture

class ks_Browser(Browser):

    '''ks_website={}
    ks_website['handbags']=[]
    ks_website['handbags'].append("https://www.katespade.com/handbags/")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=31")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=60&start=31")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=90&start=31")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=120&start=31")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=150&start=31")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=180&start=31")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=210&start=31")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=240&start=31")
    ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=270&start=31")
    ks_website['wallets']=[]
    ks_website['wallets'].append("https://www.katespade.com/wallets/")
    ks_website['wallets'].append('https://www.katespade.com/wallets/?sz=30&start=30&format=page-element&instart_disable_injection=true')
    ks_website['wallets'].append('https://www.katespade.com/wallets/?sz=30&start=60&format=page-element&instart_disable_injection=true')
    ks_website['wallets'].append('https://www.katespade.com/wallets/?sz=30&start=90&format=page-element&instart_disable_injection=true')
    ks_website['sale']=[]
    ks_website['sale'].append('https://www.katespade.com/sale/handbags/')
    ks_website['sale'].append('https://www.katespade.com/sale/handbags/?sz=99&start=99&instart_disable_injection=true')
    ks_website['sale'].append('https://www.katespade.com/sale/handbags/?sz=99&start=198&instart_disable_injection=true')'''

    def __init__(self,user=None,password=None,band=None):
        Browser.__init__(self,user=None,password=None)
        self.ks_website={}
        self.band=band
        if band=='surprise':
            print 'download SURPRISE'
            self.ks_website['handbags']=[]
            self.ks_website['handbags'].append('http://surprise.katespade.com/handbags?sz=29&start=0&format=page-element')
            self.ks_website['handbags'].append('http://surprise.katespade.com/handbags?sz=29&start=29&format=page-element')
            self.ks_website['handbags'].append('http://surprise.katespade.com/handbags?sz=59&start=29&format=page-element')
            self.ks_website['handbags'].append('http://surprise.katespade.com/handbags?sz=89&start=29&format=page-element')
            self.ks_website['handbags'].append('http://surprise.katespade.com/handbags?sz=119&start=29&format=page-element')
            self.ks_website['handbags'].append('http://surprise.katespade.com/handbags?sz=149&start=29&format=page-element')
            self.ks_website['wallets']=[]
            self.ks_website['wallets'].append('https://surprise.katespade.com/on/demandware.store/Sites-KateSale-Site/en_US/Search-Show?cgid=wallets')
            self.ks_website['accessories']=[]
            self.ks_website['accessories'].append('https://surprise.katespade.com/on/demandware.store/Sites-KateSale-Site/en_US/Search-Show?cgid=accessories')
        else:
            self.ks_website['handbags']=[]
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=31")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=61")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=91")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=121")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=151")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=181")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=211")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=241")
            self.ks_website['handbags'].append("https://www.katespade.com/handbags/?sz=30&start=271")
            '''self.ks_website['wallets']=[]
            self.ks_website['wallets'].append("https://www.katespade.com/accessories/wallets-wristlets/")
            self.ks_website['wallets'].append('https://www.katespade.com/accessories/wallets-wristlets/?sz=30&start=30&format=page-element&instart_disable_injection=true')
            self.ks_website['wallets'].append('https://www.katespade.com/accessories/wallets-wristlets/?sz=30&start=60&format=page-element&instart_disable_injection=true')
            self.ks_website['wallets'].append('https://www.katespade.com/accessories/wallets-wristlets/?sz=30&start=90&format=page-element&instart_disable_injection=true')
            self.ks_website['sale']=[]
            self.ks_website['sale'].append('https://www.katespade.com/sale/handbags-wallets/')
            self.ks_website['sale'].append('https://www.katespade.com/sale/handbags-wallets/?sz=99&start=99&instart_disable_injection=true')
            self.ks_website['sale'].append('https://www.katespade.com/sale/handbags-wallets/?sz=99&start=198&instart_disable_injection=true')'''


        self.headers['Host'] = 'www.katespade.com'
        self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        self.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
        self.headers['Upgrade-Insecure-Requests'] = '1'
                    
    def get_category_soup(self):
        category_soup={}
        for key in self.ks_website:
            category_soup[key]=[]
            for url in self.ks_website[key]:
                i=1
                soup=self.get_page_soup(url, 'POST')
                while soup=='False':
                    soup=self.get_page_soup(url, 'POST')
                    i=i+1
                    print i;
                category_soup[key].append(soup)
            print self.ks_website[key]
            print "done"
        return category_soup
    
    def get_bag_urls(self,category_soup,r):
        bags_urls={}
        #tag=soup.find_all('a',attrs={"class":"cloudzoom"})
        for key in category_soup:
            bags_urls[key]=[]
            for soup in category_soup[key]:
                try:
                    products=soup.find_all('a',attrs={'class':'name-link'})
                    tags=soup.find_all('a',attrs={'class':'thumb-link'})
                    print 'length'
                    print len(products)
                except:
                    print soup
                if len(products)==0:
                    print 'no soup found'
                    continue
                for p in products:
                    name=p.get_text()
                    name=key+'_'+name.strip()
                    print(name)
                    href=p.get('href')
                    if not href.startswith('http'):
                        if self.band=='surprise':
                            href='https://surprise.katespade.com'+href.strip()
                        else:
                            href='https://www.katespade.com'+href.strip()
                    bags_urls[key].append(href)
        return bags_urls
    
    '''def get_bag_urls(self,category_soup):
 
        #return a dict which contains the bags' url

        bags_urls={}
        #tag=soup.find_all('a',attrs={"class":"cloudzoom"})
        for key in category_soup:
            bags_urls[key]=[]
            for soup in category_soup[key]:
                try:
                    tags=soup.find_all('a',attrs={'class':'thumb-link'})
                except:
                    print soup
                for t in tags:
                    href=t.get('href')
                    if not href.startswith('http'):
                        if self.band=='surprise':
                            href='https://surprise.katespade.com'+href
                        else:
                            href='https://www.katespade.com'+href
                    bags_urls[key].append(href)
        return bags_urls
    '''

    def get_img_url(self,soup):
        img_url=[]
        tags=soup.find_all('a',attrs={'class':'thumbnail-link'})
        for tag in tags:
            img_url.append(tag.get('href'))
        return img_url

    def get_bag_name(self,soup,url=None):
        tags=soup.find_all('h1',attrs={'class':'product-name'})
        while tags=='' or len(tags)==0:
            print 'no name tags'
            print url
            soup=self.get_page_soup(url, 'POST')
            while isinstance(soup, str):
                print soup
                soup=self.get_page_soup(url, 'POST')
            tags=soup.find_all('h1',attrs={'class':'product-name'})
            print len(tags)
        name=tags[0].get_text()
        name=name.strip()
        name=name.replace('\"','_')
        name=name.replace('\'','_')
        name=name.replace(u'\xf1','_')
        name=re.sub(r'[^\x00-\x7F]+','#', name)
        return name
        
        '''tags=soup.find_all('img',attrs={'itemprop':'image'})
        if len(tags)==0:
            tags=soup.find_all('h2',attrs={'class':'product-name'})
            if len(tags)==0:
                name='fuck'
                return name
            else:
                name=tags[0].get_text()
                name=name.strip()
                return name
        name=tags[0].get('alt')
        name=name.split(',',-1)[0]
        print name
        name=name.replace('\"','_')
        name=name.replace('\'','_')
        name=name.replace(u'\xf1','_')
        return name
        '''

    def get_bag_color(self,soup):
        tags=soup.find_all('ul',attrs={'class':'swatches'})
        count=0
        while len(tags)==0:
            tags=soup.find_all('ul',attrs={'class':'swatches'})
            count+=1
            print count
            if count==10:
                print soup
                break
        nexttag=tags[0].find_all('li',attrs={'class':'selected'})
        target=nexttag[0].find_all('span',attrs={'class':'title'})
        '''color=tags[0].get('alt')
        print color
        color=color.split(',',-1)[1]
        '''
        
        color=target[0].get_text()
        color=color.replace('"','_')
        return color

    def get_color_page(self,soup):
        color_page=[]
        tags=soup.find_all('a',attrs={'class':'swatchanchor'})
        if tags is not None:
            for tag in tags:
                color_page.append(tag.get('href'))
                print tag.get('href')
        return color_page

    def get_bag_details(self,soup,Path):
        tag=soup.find_all('div',attrs={'class':'short-left'})
        if len(tag)!=0:
            tag=tag[0]
        else:
            return False
        i=0
        for t in tag.contents:
            if 'SIZE' in t:
                details=t.nextSibling
                i=1
        if i==0:
            tags=soup.find_all('div',attrs={'class':'short-right'})
            for tag in tags:
                details=tag.contents[1]
        file_name=self.name+'.txt'
        path=os.path.join(Path,self.name,file_name)
        f=open(path,'wb')
        f.write(str(details))
        f.close()
        return True

        
    def get_color_img(self,soup):
        color_image_url={}
        tags=soup.find_all('a',attrs={'class':'swatchanchor'})
        if tags is not None:
            for tag in tags:
                try:
                    img_content=tag.contents[1]
                except:
                    img_content=tag.contents[0]
                img_color_url=img_content.get('src')
                img_color_url=re.sub('\$.*\$','',img_color_url)
                color_name=tag.contents[1].get('alt').replace('/','_')
                color_name=color_name.replace('"','_')
                color_image_url[color_name]=img_color_url
        return color_image_url


class Coach_Browser(Browser):

    login_page="https://www.coachoutlet.com/store/default/customer/account/loginPost/"
    coach_website=[]
    coach_website.append("https://www.coachoutlet.com/store/default/")

    def get_category_url(self,url):
        category_dict={}
        soup=self.get_page_soup(url)
        while soup=="False":
            soup=self.get_page_soup(url)
        tags=soup.find_all('li',attrs={'class':'level1'})
        for tag in tags:
            link=tag.contents[1]
            name=link.contents[0].get_text()
            if name=="ACCESSORIES" or name=="MEN" or name=="Bags":
                category_dict[name]=[]
                category_dict[name].append(link.get("href"))
        return category_dict

    def add_urls(self,category_dict):
        for urls in category_dict:
            new_urls=re.sub("\?.*","?p=2",category_dict[urls][0])
            category_dict[urls].append(new_urls)
        return category_dict

    def get_category_urls(self,category_dict):
        category_url={}
        for names in category_dict:
            category_url[names]=[]
            for urls in category_dict[names]:
                soup=self.get_page_soup(urls)
                while soup=="False":
                    soup=self.get_page_soup(urls)
                bag_tags=soup.find_all('div',attrs={'class':'grid-container'})
                for bag_tag in bag_tags:
                    bag={}
                    out_stock="False"
                    contents=bag_tag.contents
                    for content in contents:
                        if content=="\n":
                            continue
                        if content.find_all('div',attrs={'class':'out-of-stock'}):
                            out_stock="True"
                        if content.find_all('a'):
                            url=content.find_all('a')[0].get("href")
                            bag[url]=out_stock
                            category_url[names].append(bag)
        return category_url
            
    def get_img_url(self,soup):
        img_urls=[]
        tag=[]
        #tag=soup.find_all('a',attrs={"class":"cloudzoom-gallery-active cloudzoom-gallery"})
        tags=soup.find_all('a',attrs={'class':'cloudzoom-gallery'})
        for t in tags:
            tag.append(t)
        for t in tag:
            data_cloudzoom=t.get("data-cloudzoom")
            a=re.findall("https:.*',",data_cloudzoom)
            img_urls.append(re.sub("',","",a[0]))
            
        #print len(img_urls)
        return img_urls

    def get_bag_name(self,soup):
        tags=soup.find_all('div',attrs={'class':'product-name'})
        a=tags[0].find_next('h2')
        name=a.string
        return name

    def get_bag_color(self,soup):
        tags=soup.find_all('span',attrs={'class':'swatch-color'})
        color=tags[0].string
        return color

    def get_color_img(self,soup):
        tags=soup.find_all('div',attrs={'class':'current'})
        color_urls=tags[0].get('style')
        color_urls=re.findall("https:.*\$",color_urls)
        return color_urls[0]

    def get_bag_details(self,soup,Path):
        tags=soup.find_all('div',attrs={'class':'description'})
        file_name=self.name+'.txt'
        path=os.path.join(Path,self.name,file_name)
        details=tags[0].contents
        f=open(path,'wb')
        content=str(details[1])
        content_list=content.replace("</li>","").replace("</div>","").split('<li>',-1)
        for con in content_list:
            if "<" in con:
                continue
            f.write('<li>'+con+'</li>')
        f.close()

                
    def get_url_from_txt(t):
        f=open(t,'r')
        text=f.read()
        fields=[]
        for i in text.split('\n',-1):
            fields.append(i)
        f.close()
        return fields

class test_Browser(Browser):
    ks_website={}
    ks_website['handbags']=[]
    ks_website['handbags'].append("https://www.katespade.com/handbags/view-all/")
    ks_website['handbags'].append("https://www.katespade.com/handbags/view-all/?sz=99&start=99&instart_disable_injection=true")
    ks_website['wallets']=[]
    ks_website['wallets'].append("https://www.katespade.com/accessories/wallets-wristlets/")
    ks_website['sale']=[]
    ks_website['sale'].append('https://www.katespade.com/sale/handbags-wallets/')
    ks_website['sale'].append('https://www.katespade.com/sale/handbags-wallets/?sz=99&start=99&instart_disable_injection=true')
    ks_website['sale'].append('https://www.katespade.com/sale/handbags-wallets/?sz=99&start=198&instart_disable_injection=true')

    def __init__(self,user=None,password=None,band=None):
        Browser.__init__(self,user=None,password=None)
        self.band=band
        if band=='surprise':
            print 'download SURPRISE'
            self.ks_website={}
            self.ks_website['handbags']=[]
            self.ks_website['handbags'].append('https://surprise.katespade.com/on/demandware.store/Sites-KateSale-Site/en_US/Search-Show?cgid=handbags')
            self.ks_website['wallets']=[]
            self.ks_website['wallets'].append('https://surprise.katespade.com/on/demandware.store/Sites-KateSale-Site/en_US/Search-Show?cgid=wallets')
            self.ks_website['accessories']=[]
            self.ks_website['accessories'].append('https://surprise.katespade.com/on/demandware.store/Sites-KateSale-Site/en_US/Search-Show?cgid=accessories')
            
    def get_category_soup(self):
        category_soup={}
        for key in self.ks_website:
            category_soup[key]=[]
            for url in self.ks_website[key]:
                i=1
                soup=self.get_page_soup(url, 'POST')
                while soup=='False':
                    soup=self.get_page_soup(url, 'POST')
                    i=i+1
                category_soup[key].append(soup)
        return category_soup
    
    def get_bag_urls(self,category_soup):
        bags_urls={}
        #tag=soup.find_all('a',attrs={"class":"cloudzoom"})
        for key in category_soup:
            bags_urls[key]=[]
            for soup in category_soup[key]:
                try:
                    products=soup.find_all('a',attrs={'class':'name-link'})
                    tags=soup.find_all('a',attrs={'class':'thumb-link'})
                except:
                    print soup
                for p in products:
                    name=p.get_text()
                    name=key+'_'+name.strip()
                    href=p.get('href')
                    if not href.startswith('http'):
                        if self.band=='surprise':
                            href='https://surprise.katespade.com'+href.strip()
                        else:
                            href='https://www.katespade.com'+href.strip()
                    
                    db_href=r.get(name)
                    if db_href!=href:
                        r.set(name, href)
                        bags_urls[key].append(href)
        return bags_urls