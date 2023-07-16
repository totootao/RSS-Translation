# coding:utf-8 
import configparser
import datetime

import requests
from pygtrans import Translate
import xml.etree.cElementTree as et
import os
import hashlib
import dacankao
import jinja2

import shishijuhe


def get_md5_value(src):
    _m = hashlib.md5()
    _m.update(src.encode('utf-8'))
    return _m.hexdigest()
    
config = configparser.ConfigParser()
config.read('test.ini',encoding='utf-8')
secs=config.sections()



def get_cfg(sec,name):
    return config.get(sec,name).strip('"')

def set_cfg(sec,name,value):
    config[sec][name]='"%s"'%value

def get_cfg_tra(sec):
    cc=config.get(sec,"action").strip('"')
    target=""
    source=""
    if cc == "auto":
        source  = 'auto'
        target  = 'zh-CN'
        
         
    else:
        source  = cc.split('->')[0]
        target  = cc.split('->')[1]
    return source,target


# config['url']={'url':'www.baidu.com'} #类似于字典操作
 
# with open('example.ini','w') as configfile:
#     config.write(configfile)

BASE=get_cfg("cfg",'base')
try:
    os.makedirs(BASE)
except:
    pass
links=[]
def tran(sec):
    out_dir= BASE + get_cfg(sec,'name')
    url=get_cfg(sec,'url')
    max_item=int(get_cfg(sec,'max'))
    old_md5=get_cfg(sec,'md5')
    source,target=get_cfg_tra(sec)
    global links

    links+=[" - %s [%s](%s) -> [%s](%s)\n"%(sec,url,url,get_cfg(sec,'name'),out_dir)]


    GT = Translate()

    r = requests.get(url, verify=False)
    r.encoding = "utf-8"
    html_doc = r.text
    new_md5= get_md5_value(html_doc)


    if old_md5 == new_md5:
        return
    else:
        set_cfg(sec,'md5',new_md5)
    # move style

    root = et.XML(html_doc)
    for item in root.iter("title"):
        print(item.text)
        item.text = GT.translate(item.text, target=target, source=source).translatedText
        print(item.text)
    for item in root.iter("description"):
        item.text = item.text.replace('&lt;', '<').replace('&gt;', '>')
        print(item.text)
        item.text = GT.translate(item.text, target=target, source=source).translatedText
        print(item.text)

    content = et.tostring(root).decode('utf-8')

    with open(out_dir,'w',encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write(content)

    print("GT: "+ url +" > "+ out_dir)

if datetime.datetime.now().hour%2==0 and datetime.datetime.now().minute<12:
    for x in secs[1:]:
        tran(x)
        print(config.items(x))

f = open("rss.xml",encoding="UTF-8")
contentrssxml = f.read()
template = jinja2.Template(contentrssxml)


with open('rss/dacankao.xml','w',encoding="UTF-8") as fdacankao:
    fdacankao.write(template.render(dacankao.ctx(44)))

f = open("rss.xml", encoding="UTF-8")
contentrssxml = f.read()
template = jinja2.Template(contentrssxml)

with open('rss/shishijuhe.xml', 'w', encoding="UTF-8") as fdacankao:
    fdacankao.write(template.render(shishijuhe.ctx(category='wechatefb')))

with open('test.ini','w') as configfile:
    config.write(configfile)



YML="README.md"

f = open(YML, "r+", encoding="UTF-8")
list1 = f.readlines()           
list1= list1[:13] + links

f = open(YML, "w+", encoding="UTF-8")
f.writelines(list1)
f.close()