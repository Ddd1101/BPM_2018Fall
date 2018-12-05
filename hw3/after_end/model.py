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
    user = json.loads(res.text)
    print(user['User'][0]['name'])
    res = ""
    if name == user['User'][0]['name']:
        return res
    tmp = requests.post('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/article', param)
    res = json.load(tmp.text)
    print(res['id'])
    return res['id'];

def do_login(param):
    res = requests.get('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/')