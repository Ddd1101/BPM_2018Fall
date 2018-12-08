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
    rt = json.loads(res.text)
    if len(rt['User'])!=0:
        rt['User'][0].pop('password')
    return rt['User'][0]

def do_article_submit(param):
    content = param['title']
    gfw = DFAFilter()
    gfw.parse("keywords")
    res = gfw.filter(content, "*")
    param['title'] = res

    content = param['description']
    res = gfw.filter(content, "*")
    param['description'] = res

    content = param['body']
    res = gfw.filter(content, "*")
    param['body'] = res

    _param = json.dumps(param)
    response = requests.post(url+'/Article/', _param)

    print(type(response.getcode()))
    return response

def do_article_update(param):
    gfw = DFAFilter()
    gfw.parse("keywords")
    for key in param:
        if key == 'title' or key == 'description' or key == 'body':
            res = gfw.filter(param[key],'*')
            param[key] = res
    _param = json.dumps(param)

    find = requests.put(url+'/Article/?Article.userid='+_param['userId']+'& Article.title='+_param['title'])

    find_ = json.loads(find.text)

    res = requests.put(url+'/Article/'+find_['userId'], _param)

def do_article_delete(param):
    res = requests.delete(url+'/Article/'+param['id'])
    res = json.loads(res.text)
    print(res)

def do_article_get(param):
    return 0

def do_comment_commit(param):
    content = param['body']
    gfw = DFAFilter()
    gfw.parse("keywords")
    gfw.filter(content, "*")

    param['body'] = content

    res = requests.post(url+'/Comment', param)

def do_comment_delete(param):
    res = requests.delete(url + '/Comment/', param["id"])