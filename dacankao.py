from xml.dom.minidom import parseString
from utils import fetch
import requests

domain = 'http://www.dacankao.com/'

def parse(post):
    item={}
    item['title'] = post.getElementsByTagName('title')[0].childNodes[0].data
    item['link'] = post.getElementsByTagName('link')[0].childNodes[0].data
    item['pubDate'] = post.getElementsByTagName('pubDate')[0].childNodes[0].data
    item['author'] = post.getElementsByTagName('author')[0].childNodes[0].data
    item['description'] = fetch(post.getElementsByTagName('link')[0].childNodes[0].data).css('td.t_f').get().replace('\n','').replace('\r','')
    return item

def ctx(category=''):
    url=f'{domain}forum.php?mod=rss&fid={category}&auth=0'
    tree=parseString(requests.get(url,verify=False).text).documentElement
    posts=tree.getElementsByTagName('item')
    items= list(map(parse,posts))

    return {
        'title':'大参考',
        'description':'通过全球政治经济评论,预知世界局势发展,把握外汇期货证券行情运行趋势,为您的生活理财服务。',
        'link':'http://www.dacankao.com/',
        'author':'totootao',
        'items':items
    }

if __name__ == '__main__':
    cc=ctx(category='44')
    print(cc)
