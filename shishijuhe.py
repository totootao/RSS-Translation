import re
from xml.dom.minidom import parseString

import jinja2

from utils import fetch
import requests

domain = 'https://rsshub.rssforever.com/telegram/channel/'

def parse(post):
    item={}

    description = post.getElementsByTagName('description')[0].childNodes[0].data
    list = re.findall(r'</a> <a href="(.+?)"', description)
    if not list:
        item['title']='delete'
    else:
        tree = fetch(list[0])
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
    url=f'{domain}{category}'
    tree=parseString(requests.get(url,verify=False).text).documentElement
    posts=tree.getElementsByTagName('item')
    items= list(map(parse,posts))
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

    with open('rss/shishijuhe.xml', 'w', encoding="UTF-8") as fdacankao:
        fdacankao.write(template.render(ctx(category='wechatefb')))