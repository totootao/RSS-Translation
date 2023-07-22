import json
import re
from xml.dom.minidom import parseString

import jinja2
from parsel import Selector

from utils import fetch
import requests
domain = 'https://rsshub.rssforever.com/telegram/channel/'
jsons ={}
jsont ={}
def parse(post):
    global jsons,jsont
    item={}
    description = post.getElementsByTagName('description')[0].childNodes[0].data
    list = re.findall(r'</a> <a href="(.+?)"', description)
    if not list:
        item['title']='delete'
    else:
        if list[0] in jsons:
            tree = Selector(text=jsons[list[0]])
            jsont[list[0]]=jsons[list[0]]
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
            res = requests.get(list[0], headers=headers, verify=False)
            res.encoding = "utf-8"
            res.raise_for_status()
            tree = Selector(text=res.text)
            jsont[list[0]] = res.text
        if not tree.css('span[id=copyright_logo]'):
            item['title']='delete'
        else:
            page_content= tree.css('div[id=page-content]').get()
            if page_content is None:
                item['title']='delete'
            else:
                item['description'] = page_content.replace('\n','').replace('\r','')
                item['title'] = post.getElementsByTagName('title')[0].childNodes[0].data
                item['link'] = post.getElementsByTagName('link')[0].childNodes[0].data
                item['pubDate'] = post.getElementsByTagName('pubDate')[0].childNodes[0].data
    return item

def ctx(category=''):
    global jsons,jsont
    with open('rss/link.json', 'r', encoding="UTF-8") as fs:
        txt=fs.read()
        jsons = json.loads(txt)
    url=f'{domain}{category}'
    tree=parseString(requests.get(url,verify=False).text).documentElement
    posts=tree.getElementsByTagName('item')
    items= list(map(parse,posts))

    with open('rss/link.json', 'w', encoding="UTF-8") as ft:
        ft.write(json.dumps(jsont))

    for item in items[:]:
        if item['title'] == 'delete':
            items.remove(item)
    return {
        'title':'时事聚合-原文',
        'description':'通过全球政治经济评论,预知世界局势发展,把握外汇期货证券行情运行趋势,为您的生活理财服务。',
        'link':'http://www.dacankao.com/',
        'author':'totootao',
        'items':items
    }

if __name__ == '__main__':
    f = open("rss.xml", encoding="UTF-8")
    contentrssxml = f.read()
    template = jinja2.Template(contentrssxml)

    with open('rss/shishijuhe.xml', 'w', encoding="UTF-8") as f:
        f.write(template.render(ctx(category='wechatefb')))