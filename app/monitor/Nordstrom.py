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

logger=logging.getLogger('TEST')
logger.setLevel(logging.INFO)
fh = logging.FileHandler("./app/static/log/test.log")
formatter=logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

global my_proxy  
global nordstrom_list
global lmail
nordstrom_list = {}
lmail = lucien801()
#my_proxy=None
name_list={
    4966688: "CHANEL ximiannai",
    5419480: "KIEHL'S taozhuang",
}

class Nordstrom():
    def __init__(self, url=None):
        self.basket_headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'www.sephora.com',
            'Upgrade-Insecure-Requests':'1',
            'Referer':'https://www.sephora.com/basket',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'TE':'Trailers'
        }
        self.normal_headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Cache-Control':'max-age=0',
            'Host':'shop.nordstrom.com',
            'Upgrade-Insecure-Requests':'1',
            'TE':'Trailers',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            }
        self.post_headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            "Content-Type": "text/plain;charset=UTF-8",
            'Host':'www.sephora.com',
            'Origin':'https://www.sephora.com',
            'Refer':'https://www.sephora.com',
            'Connection':'keep-alive',
            'Content-Length':'98',
            'x-o1na2nub-a':'hoSxxJXHlPRZs0gps_gq4=vuhgnqSC-5uWnxQZlA-xodX9FZURZx5olXtNHKhRZoh2sZZLyB5=gZV3x0QvDJXgyl4ocOXPyEX8uFIkKphDHgs9QJ4DxP5DHHQlHLHxvptJ2pbpEWaKFztBGMo1xpX9eTtcuGbmpDQguGePDbqJoptzyX-OrFRpgXmcpxUvHTXOdZbA2OyAlHijHZxoxxQvYm-OKBoYgxoLnXtNXpbK6_41Yk-DHr-5tBQ6uJxr0p-OKLxOAMblfEnLoSlRndSAyFoYKp4lQDXKXplqKgbp0Q19IvxDHAQOlDUwyjsKvH-vEGyp5xNKJIPB-BxOAgbhFW-nbmnvl14KXAbx0pXvPmlg_9s_qT4lPxwKfZBtK0a=qrbkXz-OgM-RuHHoyGov2Dao0XXoqiK36KyaAGazlrl9g-uJluQqUXPJDghoyjXOnp2TRtxWurQ6Bpy1xRyPKDxgRL2m0Mtr2XhDf3--erUYdjX9cM4kfA5rKN-xHExWuG-ggqBYIp-DZmoLRMJM06u_jm-OqmXbe_hgRXsPHS19ppaYkSmAxjXg-fKFo3U9OUtJrEb10PovEvopgpl10Z1N8Ms9fG-O6GX5Z-UmFGlPyNxkKGlK6GUAe6UjvpHByxXgop4tiZQ9FN59qTlklZy1fNsgsA2LKn6NFnQvHKbMBBQP_p-xxpspsZsL29aguJszyxQOqgo8yJhOu-48QS_KHJ-js1sU2C_Yy14pGBb1H0erWX4_s8_C4pn9yFQvzZf3H8n_qxxx6mxqQKbnHDbkdjs9gMsp_XnYl3oAgmnhx3QRurukf850yMHL-vovXxoYlJ_oFny10gxACxyh0Alc8Zs=yWooyJsxopsLyRNqoVKY=eognGUTnBhOAxXY6NFc8Mn99mnzyiPJvntNxhUYKx-Ol8o9vHn6cO-vHraRZWbrQZ-mxeBC4HE3yZhO_qBmFC-g6Nu_FntWpko3s5tkFqu0HJuOtoXWZj-g6JU8ZGnLyBX9cA_DHJXoHnjl0Ms10dUhvponlxKAvp59KJbxsJ-OkQbClCa9h-1hHW5vHkoUZ3QOvvx9fZmRRA_K-SVYZoSTZZnxFxUFUvb8u3-O2oKLPpQKxp_DdDblHMQgZZlDxu=lcAnv-pQKBetklYlanHdYWqxP6dyKKtW1Hr49KpTYPMeOlOXKqxxRuNQMuTbpnNyKz8Kg6YWjHThOvpUcudXU2MUOuH-OfS-xfZ-xGWlkfFX9B5xYFxn=0MB3H0QOlZWXRZnv0ZXxQWsYLnu_owogydat0psPlWtOgpXTRMoJeXQn_XxOfCqqlM=KQqnFe3n=0ZU36MscpxxWZn4oOmX=yJuvd8HzyJ4MyJxgAzuQfJ-0IHWNHdsqcxoOgqoLyFn9fFyNZJbAgulfsHKkZZnR8Zs30MX1xxlmHw2Lx54lHZl9FFQvHNXC-xB3qXs9dDukPpeOdxHxHZy9yFs9gH-v6FyWuxbJJB-v-vX=gZ4_yBtkzm-RZxowEPtkBGoOgxtkKpDFWvx9flU8Hx6N0pbTnePNHAXBZWUqfN-OfYx9du_=qdXF_mbz0P-gyLbJ-vsDZNS10pnElObL90bOfLxJHuXx0MsFyFXonp8g6mPknps9qTbDXG_mHZbYTZeqrxmk80=PFZ_WZqQjqxXK6LaAQZn3xlQtF84lcZnn6T4Wn3og8poM2XbC6Rooxp4_FdaSFjQ96MDxHq4ltMbjyWXv01BCZnb=Dx5g8XoDFAU3vphRuTQW8pbk6MuhHZ41xNl0nhNqtktzn3bFpp-zsEoOGgKJEFPkBeUNHrhgyJovUSljD-5Pum-DHAcJXHbrcpsu8X41HN_n4xs9PAPzyMPr6jsU2m23vpXxTMsJB5lDHVHDm3-D0Ms1IDQDEx51Zr5o6n4PyZXDdGakfF5P5ixqcDhOdghgyFthx3bNHeUFZuHAAxQkfJm6TpUr63X=HEe04gslxNPt6TDYljSveTtMyqoDHZs9dM_YPD-04H-qlvN5xxjPHxaYkh-v-pI9qxo_GJya6Cs_qEoqfP_x0D1OFXsNHJb9K0NKdxRO-MQRZYtBZGX1mGbnGFeJkmUBitlLPp_10Do=qwX-PDsjgp=RylacZJxPnsDLnplkuosOs0lJxxbMOm_zAjb8eJ2YLX43vSepGFD3oihRnpnWZJxFlrdpGxtMsZsbrZbmDHblfTbhHNaaGHorlmUkBShOnxogyN-vvXVKHWZknp2g_ZXPRM5OgMXYIZXoHJy98AjWWXs=xvuzfFxgyHQWnGsltTuM6zsPyT-OfxoUe8LOtHslu1_9txMpqNoz2t5OflbktxU_pmaK2ZoxuxQOop4WREsQyrs=HAZkKvX=6dXYFYsr6CoLLgUD06sKeIX=xuXO4vDRpHXAem_0qFo50MXOPZXDxMmDDZDL6NBjH3XvegoKHuUt20tNprSCne5oq3sPrdUYGmXOFTy1Hgs9OCxkppXq6nQglNlqlg49Ues1HMhljm-Of1LmHFUYgpUOr1FrjObcu3UATMQOuGhjvHSLQ-BmyFXUH8-jHZtB0Z_0gwPBqx-OuJpjgXQjqDU3qrbkLw-6rNtMppeglAPJeGQjHTngHXQx6x-qu1oOXx-nsr4=xHPhHMQ=6fUnHToPyMol6Gn9_XeP6LDW8pSABpn52pBYNmXxHToKxNojvAHFUTxRumkMHW4blZDhxo_EFFoL2MoAeRbY-Mh9lEjKIp4P0ZUFApyoSruYdF49eLtfun4_npYJ6Z2LHq4zHGB10Mn1xY_hHShxwnJrOmbQsMa_mmlj0Mbx2Yo-T2BDFPkRRXbk8pHqfmbYyGyzHWoDHNd86jxqxN0Tfm2YPy9vHnBPyYq0pp8DHgB3iAnjsq_Od_Xw6e4ABD-jgBx1x5BLRpDOXpnKdNtkMYla6Jn9Fy_v6Jsp6_st6BK0RjKYFE_gl_PNdNXKNmQ9RYQDdMQgugy9lAllfAQOlZog6FdhO8lRuTXWuJXYBMs9qjhqfKJt6N4=HFl9PmXlUCbLyuaOqTUKxKQ1IXnA0psl2Dl9gZPNZnXx2pbkvHjCZEQDMZbkrLXp0M-RZ3UMQyQq2X4KlFsTundDX0eO6TPrH29x8ZQvWMK3HxSmxpQqQGKLPm_J6Zk_LMdOdgXPnS-DLXuKxpdgLX5oGWQxCDB9-x8-Q8XW_CKkzY5q6woPRpbhJHnmxpxmHgoYfftdMY9nsLX9slxWu_-56jKORB4Ps-QDQEyWujL9uj-DxpQxqT-DHdaPoG510X-0GDPB0XbmHTtByjbUUpUkKvSTuRoU8MXOgMsa6Ay9Fzurxf_kq8yUPZUOuWbzyJ49Pp=9ENU8WpuHp5KzlZXv-pQx6Hb3Hl--Hx4zyTXoGwumxpo3qSsnSktcRd-RuS4rKxy=HJ5OJDUBdly=Hr-xxJ2PHnQ6dm1tCphxnC499i_9qNoLlGhvQ84tUpaoqJ4=qxxDxzjl6GS3H9xmHNXF0pUYf11zWpBYBpQ_u3ntW6bP_MHvPpbBPmnwLp_PlFXKHZKpqM5vI0UmHBoNHDlP4xDL68A=gm4_6K5PlJPk9msl6NbOtp-vqTUJUGbJB=boqMa_z0oOvnSCK52pAxl1HTh-Z3=oOB-vHNx1FW5O_BuBMXXPoB=Zb3tCRpavQDxoU0a_6WXzCpnhv5KCEeogoqUBHCjMgMag6o-0W1PNxD-0qFb3H9XPy849sDBPlX_nyMQ9em-jsJcJl8u9nDnxJpQOqmKcAxbklrBOKMoOIXj_l859JosRUxokdC-06ZDhvnf9BHsWZ3xK6xtV6TQ-pHhOFAXqyNUBSBDAHabqkm_goM_YeKx0uxbA2ZhO6Tq1HGXKppoYIUx9gXUw2goSWmbkllol0p49XD-q6F-00pLkld=Y6JbpvBO8HJbqfXbNHGtR8xD8KM=1xBslxpUYqZWjqZUFcZox2p-vzZSTRX4=6EK0qG4oHMKpxB_Ffxu0ux-Dx6_DddQl6J-OKkhR04s9yA2Y_BuNfnaWRwTmHwtNcpHXGnX8X5e9ygN9PD_0yx-jaqbOBxnRuJoOcm=nHAUzuM_ogXSiHB4KHNUT8p-Ocq_g4pPBxpUv-k0p0A6KN6sv2MQFfEdqlMaOgybmHGX=Hxsovn-vqJbgApb3HL-qlqnLLZaPsxRYdo_Fl3XYXvdgok09nxjNx6B=6muAHJuTRpKoq4X8JpnAFZ_jyD0YqT-jgGtcuP-gFKXaH1S3H1xoHENoG1-gyEX_gyhOnxUL6ZtOnlPJrJthqDUmDGbj0MKMdwXFcv9g-5sKgOXRZNoFZ3lg6FyW8AlMHbjg-x_V2X_vgpDgopsoqTUJdJQ1HDo0QPKOeubLop4kPXRD0ksllWQ9drnzyZNhHio9qA4kgMu3HS48qAaOuZXFFPQOPMsUxhdxlTSA0ZHAFAxPxpQ9q1W9dn=qlxxqxjSDHRxKMZS3vvSYuo-Ozpxo0pPzHxymHCb56qUmcds=gp_3HY4W8msJ6xhOnp_0K3b10X_Cl2QqPCh0qT4XGiscuMhOy851HB49IEDkqSnv61Xm0yKg6DB2tpnqx0noQCSFyNs9LAXDxrbEoxTFuxykETXKHCMLopo_HJmNxShOQNbLHNUBHL-x4FdNHWtMWmUYUp-jy8_PyFlP-pa50mXR8MQYl3tNFLnKHlbBdjQcul28cq28udX00M=RpG4l_XXOvp_3qR-OV-VpGF4NLZK8ETQOK0I=gtQOLZKRurbw2XSkZG-vcmXo0pbClgtJgve3Pa49IMHjHOoptzaKqx1=HFUOrDuo=kUABko9Lmog2D_vPpPgy8XDH8SAlryknSBTuZogbmu1xBn1HMKwApXAyNxP58_g1j1klNH0Z_-gKpUAeFQqfJXRuKtVeqtcRBsPlFsksZoO9-bpgOUPopPhx3IllJtMLZX=6Y1O-eiQAxoOgqKYFFuYcZoTqoDYlCxzymtkvxXgoHh6E--vro-gqDHxqP4krZbpwmoTRp4Wjn44eN_Rul-xGJbw6Mtr-HtRuidTZd2YMXBDXpdB8M-OqSoow-RRZZ=WuE4JHzxgKMhj5c-OlTX3qBxxIcUngpjOfT2YRp5gF1Xo2ABkpD=rWZXKqBxvxDDYeNQgoxKYZxsKlY-DHY4kfR5R8pxKeua9F9bmxxxYFM-veGuKHGhgxpXAxKtkFq_kzPQ9h0hvHSZcRRBOuTukdF_=HLuV6RtNHlsooSh_FFy9l1_oexalFBlh2XMNZxuC6FykfuDpVVXK3-QjyzDpqTbXLK-xxv9lPM=K6MBV6xU36B-D0Xb0KJsPuxy=6NU0Wp_NHKwC6G_0eiSYeFs9rX-OWM-xxpBn6HUYqZbzKppO-v-OFZKxuJsKHW=9X3x0XTPkZZZBHD5y0MUZHx1UsJnLqFQ9cM8YZ3Xve1XD0zoTRM2L6Wsv6l-D0pxDApxn0CsafZtBS0nKfD6xqRQOsZB9qMbB0MPz6WuPPpX9-vbL5Zfi8mBvfYHHXM61H_SLakxxHNn3_XyklJx56JlK4z4_6xbjWZj1HH_OXps90X-qSpXlZW4963UDHjxYXpPkRDXU63s94pXyxXKCRXX5-Bl=xpDPym9RRABp8MoDxehj_Mja6DIOuBPPyFo1HAbC6JSA6xU6eFxn6lDnlX4cujULsSs_qMcNHXsyfMXYJ4PBxI59tD-OdN=JlHsxvDXoGH4WApPzoyXP1naJBph5GDmBZdNW0ZsDZNtJdJ=KMDKNHml1xvRtbdDA-5aUxBBA6roOfX4_UHoM4RhP2p5vQRx=gMhRnH0jH3Q0nxnoo3yf6ll9-ppqlZtM2MbktpnmHGQcpe=9Ae-xqZmF2pQ6c0IK68-0PvQOEnlKtCxOfg5_xx_kpkDAeVhOcMx9yMBKRZuzy3b_qDoLRp9vBjUJQWT9lqKc8xDgbp4YZmum0M-DH-RR0mJgRBlKHBbOr--vcNsxRpQvzxuOzpaOWMyNxkocuqUmHrjRuJ-0Wv2hfRlcuZbtSH-RnpxNHh2ZZAyPyvPzuMn1AxtBMXdv2IXKHHPBGNQRtp-OKCbvH1oNHxhPyr-vBG_3HrPJDpsL-BU3xSbrfx-D0wbh-pa9ZP-vKvURu6UYfJMLujHYXM-gHxlxxpbruxnruPl9qZ-x6X4YZ8g_yKS1sNa9Fr_=xhez_ZdcnMsL8ZX=1bHg8Zaa-zNF6Ml0n5xg6u_vHKxqtxsKxdRO2X_lTM_OvJuoGqXRFWtJ6Za=Hrsx6FXOcZPeeCD3HxQOdu_jrNoJrrtzLLnn6g_vWdULuAXv0MxAdzBx6SIWZqX9AHbLu2mAr_wllzxg-vsKf-JLRE-g_OIOXpl_6udFtSbN8px_0AsMWpQMQjxnxeyx0ExObHROJDUjHAXvuHX8vpyk-0iKxk=K5mRpxxyxGnULyl_ql9-jvDxABp9gpebr6D-OjFNp6oQOLMtDZNaAxM-OrZ_LyMXLyDQqfF4o-0axOIPkPql=HmkjqTaD8p=RuNlrfF4oUpx1QHUIEJbvqFtkoShvdnukFDbBr3bO6nhj6js9dx-OdDX0x-svUdb1tp5Kn24zxMQ1xpsFHTPk5FxWZW-jKS-OlMb0QgUL8vQvfj-xxSMUqFhRZ8cZHW4kcp4QkTBgyTzYvGtVlW-xvFhxHJlK2plYZn4MxebYvv_Bu6oRpxV80w-g6BsWuZmrZDbC-5WOSLaRu8tMoe_RZqXDppo1xDtJiAoDH8oWuC4ly1-vEq_3yNBjoB-gy3bDxM4TpzsmLpbN0X-n634f6WhqcZXOfWb3-Dx9vH9TpGUpUrRr_MRYMAs9bpuOQ3xNFNsKHJPkzvUHb-m4KxHKHrRjHDeh61XW0X4BGq_B6CsOn6S30wl1HStrv5X06N2pGWhx2HXDHNxOcXlnHYUkvpUDqE4BHK9vMpLPyA4ky_=gFxyz6EUzA',
            'x-o1na2nub-b':'28mo6d',
            'x-o1na2nub-c':'AICkbbZqAQAAnKVe1GuAwghJBP8qRhTmEhAjMmIb0c8-KBFrQgAr8j_6KsJG',
            'x-o1na2nub-d':'0',
            'x-o1na2nub-uniqueStateKey':'A4t2hbZqAQAAW-9GLzoeelVYB64Wzg7vRWTTqlgeWWzyldc95q7cgkg1UooGAawUMfCuchAEwH8AAEB3AAAAAA=='
            }
        self.url = url
        print self.url
        self.ID = int(self.get_id())
        print self.ID
        if self.ID in name_list.keys():
            self.name = name_list[self.ID]
        else:
            self.name = self.get_soup().find_all('span', attrs={'class':'_2JGWw'})[0].get_text()
        print self.name

    def get_id(self,):
        if '?' in self.url:
            self.url = self.url.split('?')[0]
        item_id = self.url.split('/', -1)
        if not item_id[-1].isnumeric():
            item_id = item_id[-2]
        return item_id

    def get_soup(self):
        response_code = 0
        while response_code != 200:
            try:
                response = requests.get(self.url, headers=self.normal_headers)
                response_code = response.status_code
            except Exception, e:
                print e
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def get_status_by_url(self, color=None):
        color_list = []
        soup = self.get_soup()
        if color == "":
            color = None
        if color is None:
            add_button = soup.find_all('button', attrs={'class':'_2xKC5'})
            if len(add_button) > 0:
                return True
            else:
                return False
        else:
            color_ul = soup.find_all('ul', attrs={'class':'_1aALu'})[0]
            color_ils = color_ul.contents
            for item in color_ils:
                color_list.append(item.find_all('span', attrs={'class':'_1zgoP'})[0].get_text())
            if color in color_list:
                return True
            else:
                return False

class pNordstrom(Nordstrom):
    def __init__(self, url, color):
        Nordstrom.__init__(self, url)
        if color is None:
            self.color = ""
        else:
            self.color = color
        self.ID = str(self.ID) + str(self.color)
        if self.ID in nordstrom_list:
            self.duplicate = True
        else:
            self.duplicate = False
        self.status = self.get_status_by_url(self.color)
        self.info = [self.ID, self.name + ' ' + str(self.color), self.url, str(self.status)]
        print self.info
        logger.info('Nordstrom {0} the status is {1}'.format(self.ID, self.status))
        nordstrom_list[self.ID] = self.info

    def process(self):
        global nordstrom_list
        global lmail
        if self.duplicate:
            return
        count = 0
        while self.ID in nordstrom_list:
            if count == 100:
                count = 0
                print "Nordstrom {0} is ongoing".format(self.ID)
            count += 1
            time.sleep(5)
            try:
                status = self.get_status_by_url(self.color)
                if status != self.status:
                    self.status = status
                    nordstrom_list[self.ID] = self.info
                    logging.info('Nordstrom {0} {1} the status change to {2}'.format(self.name, self.color, self.status))
                    if status==True:
                        m = '{2} Nordstrom {0} {1} the status change to available \n {3}'.format(self.name, self.color, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.url)
                        lmail.sm('Nordstrom', m)
                self.info[3]=str(status)
            except Exception, e:
                print self.ID
                print e
