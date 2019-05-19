import requests
import json
import re

class sender():
    def __init__(self, url=None):
        self.url=url
        self.product_id=""
        self.queryurl=""
        self.color_id=self.get_color_id()
        self.data={}
        self.post_headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept':'application/json, text/plain, */*',
            'Accept-Encoding':'gzip, deflate, br',
            'Host':'www.michaelkors.com',
            "Content-Type": "application/json; charset=UTF-8",
            }
        self.get_headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            #'Cache-Control':'max-age=0',
            'Connection':'keep-alive' ,  
            'Host':'www.michaelkors.com',
            #'If-None-Match':'W/"155fe0-59GwHtFv8n7gzAhlWJyOTyPD80M"',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            }      
    
    def get_product_id(self):
        bag_id = re.findall("R-US.*", self.url, 0)
        bag_id = bag_id[0]
        if "?" in bag_id:
            bag_id = bag_id.split("?")[0]
            bag_id=bag_id.split("-")[1]
        return bag_id
        
    def get_color_id(self):
        return self.url.split("color=")[1]
    
    def set_postheaders(self, key, value):
        self.post_headers[key]=value
        
    def set_data(self,key, value):
        self.data[key]=value
        
    def do_sendjson(self):
        self.response = requests.post(self.refer, data=json.dumps(self.data),headers=self.post_headers).json()
    
    def do_get(self,url=None):
        if url==None:
            url=self.queryurl
        print url
        return requests.get(url, headers=self.get_headers)
    def if_available(self):
        #print self.response["statusMessage"]
        if self.response["statusCode"]==200 and "added" in self.response["statusMessage"]:
            return True
        else:
            return False
        
    
class MK(sender):
    def __init__(self, bag_url):
        sender.__init__(self,bag_url)
        self.ifavailable=False
        self.refer = "https://www.michaelkors.com/server/addToCart"
        self.product_id = self.get_product_id()
        self.queryurl="https://www.michaelkors.com/server/productinventory?productList=" + self.product_id
        self.skuid = self.get_skuid()
        self.set_postheaders('Referer',self.url)
        self.data={"productId": self.product_id, "skuId": self.skuid, "quantity": "1"}

    def get_skuid(self):
        a=  requests.get(self.url,headers=self.get_headers)
        f=open("temp.txt","w+")
        for l in a.iter_content(1024):
            f.write(l)
        f.close()
        count=0
        with open("temp.txt","r") as f:
            for line in f:
                temp = re.findall("INITIAL_STA.*Other", line, 0)
                if len(temp)!=0:
                    break
        temp_list=re.findall('{"identif.*?]}}',temp[0],0)
        print self.color_id
        for i in temp_list:
            if str(self.color_id)+'"' in i:
                temp_id= re.findall('identif.*?",',i)
                break
        for id in temp_id:
            id=id.split('":"')[1]
            if re.findall("^\d",id):
                id = id.split('"')[0]
                if id!=self.color_id:
                    return id
    
    def get_stock_status(self):
        name=self.url.split('com/')[1].split('/_')[0].replace('-', ' ')
        temp_response=self.do_get().content
        match=re.findall('{"identifier".*',temp_response)
        if len(match)!=0:
            list = match[0].split('{"identifier":')
            for l in list:
                if self.skuid in l:
                    if "In Stock" in l:
                        self.ifavailable=True
                        return [name, 'In Stock']
                    elif "Out of Stock" in l:
                        return [name, 'Out of Stock']
                    else:
                        return [name, "No info of stock"]
        