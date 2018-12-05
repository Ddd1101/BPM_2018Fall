import web
import requests
import json
from filter import DFAFilter

def do_article_filter(src):
    content = src['content']

    gfw = DFAFilter()
    gfw.parse("keywords")
    gfw.filter(content, "*")

    src['content'] = content

    requests.post('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/article', src)

def do_comment_filter(param):
    content = param['content']

    gfw = DFAFilter()
    gfw.parse("keywords")
    gfw.filter(content, "*")

    param['content'] = content

    requests.post('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/article', param)

def do_register(param):
    name = param['name']
    print(name)
    res = requests.get('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/?User.name='+name)
    print(res.text)
    user_list = json.loads(res.text)
    res = ""
    for itor in user_list[1]:
        print(itor)
        if itor['name'] == param['name']:
            return res;
    tmp = requests.post('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/article', param)
    res = json.load(tmp.text)
    print(res['id'])
    return res['id'];

def do_login(param):
    res = requests.get('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/')