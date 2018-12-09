import web
import requests
import json
import time
from filter import DFAFilter

url = 'http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS'

def do_user_register(param):
    name = param['username']
    print(name)
    email = param['email']
    res_name = requests.get(url+'/User/?User.username='+name)
    print(res_name)
    json_name = json.loads(res_name.text)
    res_email = requests.get(url+'/User/?User.email=' + email)
    json_email = json.loads(res_email.text)
    rt = ""
    if len(json_name)==0 and len(json_email)==0:
        _param = json.dumps(param)
        tmp = requests.post(url+'/User/', _param)
        rt_raw = json.loads(tmp.text)
        rt_raw.pop("type")
        rt = json.dumps({'user':rt_raw})
        print(rt)
        return rt
    else:
        return rt

def do_user_login(param):
    name = param['username']
    res = requests.get(url + '/User/?User.username=' + name)
    rt_raw = json.loads(res.text)
    rt = ""
    if len(rt_raw)!=0:
        pwd = rt_raw['User'][0].pop('password')
        if param['password']!=pwd :
            return rt
        else:
            return rt_raw['User'][0]
    else:
        return rt

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
    return response

def do_article_update(param):
    find_req = param['user']
    find_req.update(param['article'])
    update_req = param["item"]
    gfw = DFAFilter()
    gfw.parse("keywords")
    for key in update_req:
        if key == 'title' or key == 'description' or key == 'body':
            res = gfw.filter(update_req[key],'*')
            update_req[key] = res

    for key in find_req:
        if key == 'title' or key == 'description' or key == 'body':
            res = gfw.filter(find_req[key],'*')
            find_req[key] = res

    find_req_ = json.dumps(find_req)
    find = requests.get(url+'/Article/?Article.authorid='+find_req['userId']+'&Article.title='+find_req['title'])
    find_ = json.loads(find.text)
    if 'Article' in find_:
        tmp = find_['Article'][0]
    else:
        return json.dumps({"error": "something wrong in request"})

    for key in update_req:
        print(key)
        if key in tmp:
            print(key)
            tmp[key]=update_req[key]

    tmp["updateat"]= time.time()



    res = requests.put(url+'/Article/'+str(find_['Article'][0]['id']), json.dumps(tmp))
    rt = res.text
    rt = json.loads(rt)
    rt_ = json.dumps(rt)
    time_tmp = float(rt['createat'])
    rt['createat'] = time.asctime(time.localtime(time_tmp))
    time_tmp = float(rt['updateat'])
    rt['updateat'] = time.asctime(time.localtime(time_tmp))


    if res.ok :
        return json.dumps({"article":rt})
    else :
        return json.dumps({"error":"something wrong in request"})

def do_article_delete(param):
    res = requests.delete(url+'/Article/'+param['id'])
    res = json.loads(res.text)

def do_article_get(param):

    return 0

def do_aticle_list(param):
    req_state = url+"/Article/"
    it = 0

    for key in param:
        if it == 0:
            req_state = req_state + "?Article."+key+"="+param[key]
            it = it+1
        else:
            req_state = req_state + "&Article." + key + "=" + param[key]
    res_raw = requests.get(req_state)
    res = json.loads(res_raw.text)
    it = 0
    for each in res['Article']:
        it = it+1
    res.update({'articlescount':it})
    sort_var = res['Article']
    sort_var.sort(key = lambda x:x['createat'])
    for each in sort_var:
        time_tmp = float(each['createat'])
        each['createat'] = time.asctime(time.localtime(time_tmp))
        time_tmp = float(each['updateat'])
        each['updateat'] = time.asctime(time.localtime(time_tmp))
    res = json.dumps(res)
    return res

def do_comment_commit(param):
    content = param['body']
    gfw = DFAFilter()
    gfw.parse("keywords")
    gfw.filter(content, "*")

    param['body'] = content

    res = requests.post(url+'/comment', param)

def do_comment_delete(param):
    res = requests.delete(url + '/Comment/', param["id"])