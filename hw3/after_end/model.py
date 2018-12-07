import web
import requests
import json
from filter import DFAFilter

url = 'http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS'

def do_user_register(param):
    name = param['name']
    email = param['email']
    res_name = requests.get(url+'/User/?User.name='+name)
    json_name = json.loads(res_name.text)
    res_email = requests.get(url+'/User/?User.email=' + email)
    json_email = json.loads(res_email.text)
    rt = ""
    if len(json_name)==0 and len(json_email)==0:
        _param = json.dumps(param)
        tmp = requests.post(url+'/User/', _param)
        rt = json.loads(tmp.text)
        return rt['id']
    else:
        return rt

def do_user_login(param):
    name = param['name']
    res = requests.get(url + '/User/?User.name=' + name)
    rt = ""
    print(res)
    if len(res)!=0:
        tmp = res.pop('password')
        tr = json.loads(tmp.text)
    return rt

def do_article_submit(param):
    content = param['body']

    gfw = DFAFilter()
    gfw.parse("keywords")
    gfw.filter(content, "*")

    param['body'] = content

    _param = json.dumps(param)
    tmp = requests.post(url+'/article', _param)

def do_comment_filter(param):
    content = param['content']

    gfw = DFAFilter()
    gfw.parse("keywords")
    gfw.filter(content, "*")

    param['content'] = content

    requests.post(url+'/article', param)