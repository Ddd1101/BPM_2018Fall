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
    email = param['email']
    res_name = requests.get('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/?User.name='+name)
    json_name = json.loads(res_name.text)
    res_email = requests.get('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/?User.name=' + email)
    json_email = json.loads(res_email.text)
    rt = ""
    print(len(json_name))
    print(len(json_email))
    if len(json_name)==0 and len(json_email)==0:
        _param = json.dumps(param)
        tmp = requests.post('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/', _param)
        rt = json.loads(tmp.text)
        return rt['id']
    else:
        return rt

def do_login(param):
    res = requests.get('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/User/')