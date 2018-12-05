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
    json_res = json.loads(res.text)
    print(json_res)
    rt = ""
    print(len(json_res))
    if len(json_res)==0:
        print("post to db")
        print(param)
        tmp = requests.post('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/', param)
        print(tmp)
        rt = json.loads(tmp.text)
        print(rt)
        return rt['id']
    elif name == json_res['User'][0]['name']:
        return rt

def do_login(param):
    res = requests.get('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/')