import web
import requests
import json
import time
from filter import DFAFilter

url = 'http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS'

def do_user_register(param):
    dict_ = ['email','id','username','bio','image']
    name = param['username']
    email = param['email']
    res_name = requests.get(url+'/User/?User.username='+name)
    json_name = json.loads(res_name.text)
    res_email = requests.get(url+'/User/?User.email=' + email)
    json_email = json.loads(res_email.text)
    rt = ""
    if len(json_name)==0 and len(json_email)==0:
        if 'inmage' not in param:
            param.update({'image':'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2588767485,2358347029&fm=26&gp=0.jpg'})
        _param = json.dumps(param)
        tmp = requests.post(url+'/User/', _param)
        rt_raw = json.loads(tmp.text)
        rt_raw.pop("type")
        for each in dict_:
            if each in rt_raw:
                continue
            else:
                rt_raw.update({each:None})
        rt = json.dumps({'user':rt_raw})
        return rt
    else:
        return rt

def do_user_login(param):
    dict_ = ['email', 'id', 'username', 'bio', 'image']
    name = param['username']
    res = requests.get(url + '/User/?User.username=' + name)
    rt_raw = json.loads(res.text)
    rt = ""
    if len(rt_raw)!=0:
        pwd = rt_raw['User'][0].pop('password')
        if param['password']!=pwd :
            return rt
        else:
            rt = rt_raw['User'][0]
            for each in dict_:
                if each in rt:
                    continue
                else:
                    rt.update({each:None})
            return rt
    else:
        return rt

def do_profile_get(param):
    dict_ = ['email', 'id', 'username', 'bio', 'image']
    req_1 = param['user1']
    req_2 = param['user2']
    res_raw_2 = requests.get(url + '/User/?User.username=' + req_2['username'])
    res_2 = json.loads(res_raw_2.text)
    param = json.dumps({'user1': req_1['id'], 'user2': res_2['User'][0]['id']})
    res_raw_follow = requests.get(
        url + '/Follow/?Follow.user1=' + str(req_1['id']) + "&Follow.user2=" + str(res_2['User'][0]['id']))
    rt=res_2['User'][0]
    rt.pop('password')
    for each in dict_:
        if each not in rt:
            rt.update({each:None})
    res_follow = json.loads(res_raw_follow.text)
    if len(res_follow)>0:
        res_follow = res_follow['Follow']
        if len(res_follow)>0:
            rt.update({'follow':True})
        else:
            rt.update({'follow': False})
    else:
        rt.update({'follow':False})
    return rt

#2018/12/10 9.16am add taglist module by:gxhou
def do_article_submit(param):
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'passstate', 'authorid']
    content = param['title']
    gfw = DFAFilter()
    #gfw.parse("keywords")
    #res = gfw.filter(content, "*")
    #param['title'] = res

    content = param['description']
    #res = gfw.filter(content, "*")
    #param['description'] = res

    content = param['body']
    #res = gfw.filter(content, "*")
    #param['body'] = res

    has_tag = False
    taglist = ""
    if 'taglist' in param:
        has_tag = True
        taglist = param.pop('taglist')

    _param = json.dumps(param)
    response_1 = requests.post(url+'/Article/', _param)
    response_1 = json.loads(response_1.text)
    response_1.pop('type')

    for each in dict_:
        if each in response_1:
            continue
        else:
            response_1[each]=None

    time_tmp = float(response_1['createat'])
    response_1['createat'] = time.asctime(time.localtime(time_tmp))
    time_tmp = float(response_1['updateat'])
    response_1['updateat'] = time.asctime(time.localtime(time_tmp))
    articleid = response_1.pop('id')
    response_1.update({'articleid':articleid})
    if has_tag == True:
        response_to_json_1 = response_1
        aritcle_id = response_to_json_1['articleid']
        for key in taglist:
            param_tag_article = json.dumps({'articleid':aritcle_id})
            param_tag_article.update(key)
            requests.post(url + '/Tag_article/',param_tag_article)
        response_2 = json.loads(response_1.text)
        response_2.update({'taglist':taglist})
        return json.dumps({'article':response_2})
    else :
        return json.dumps({'article':response_1})

def do_article_update(param):
    dict_ = ['id','title','description','body','createat','updateat','passstate','authorid']
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
        if key in tmp:
            tmp[key]=update_req[key]

    tmp["updateat"]= time.time()

    res = requests.put(url+'/Article/'+str(find_['Article'][0]['id']), json.dumps(tmp))
    rt = res.text
    rt = json.loads(rt)
    #rt_ = json.dumps(rt)
    time_tmp = float(rt['createat'])
    rt['createat'] = time.asctime(time.localtime(time_tmp))
    time_tmp = float(rt['updateat'])
    rt['updateat'] = time.asctime(time.localtime(time_tmp))

    for each in dict_:
        if each in rt:
            continue
        else:
            rt[each]=None

    if res.ok :
        return json.dumps({"article":rt})
    else :
        return json.dumps({"error":"something wrong in request"})

def do_article_delete(param):
    res = requests.delete(url+'/Article/'+param['id'])
    res = json.loads(res.text)

def do_articles_get(param):
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'passstate', 'authorid']
    req_state = url+'/Article/'
    it =0
    for each in param:
        if it == 0:
            req_state += ('?Article.'+each+'='+param[each])
            it += 1
        else:
            req_state += ('&Article.'+each+'='+param[each])
    print(req_state)
    rt_raw = requests.get(req_state)
    print(rt_raw.text)
    res = json.loads(rt_raw.text)
    it = 0
    res['articles'] = res['Article']
    res.pop('Article')
    for each in res['articles']:
        it = it + 1
    res.update({'articlescount': it})
    sort_var = res['articles']
    sort_var.sort(key=lambda x: x['createat'])
    for each in sort_var:
        time_tmp = float(each['createat'])
        each['createat'] = time.asctime(time.localtime(time_tmp))
        time_tmp = float(each['updateat'])
        each['updateat'] = time.asctime(time.localtime(time_tmp))
        for item in dict_:
            if item in each:
                continue
            else:
                each[item] = None
    res = json.dumps(res)
    return res

def do_articles_all():
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'passstate', 'authorid']
    req_state = url+'/Article/'
    rt_raw = requests.get(req_state)
    print(rt_raw.text)
    res = json.loads(rt_raw.text)
    it = 0
    res['articles'] = res['Article']
    res.pop('Article')
    for each in res['articles']:
        it = it + 1
    res.update({'articlescount': it})
    sort_var = res['articles']
    sort_var.sort(key=lambda x: x['createat'])
    for each in sort_var:
        time_tmp = float(each['createat'])
        each['createat'] = time.asctime(time.localtime(time_tmp))
        time_tmp = float(each['updateat'])
        each['updateat'] = time.asctime(time.localtime(time_tmp))
        for item in dict_:
            if item in each:
                continue
            else:
                each[item] = None
    res = json.dumps(res)
    return res

def do_aticle_list(param):
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'passstate', 'authorid']
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
    res['articles'] = res['Article']
    res.pop('Article')
    for each in res['articles']:
        it = it+1
    res.update({'articlescount':it})
    sort_var = res['articles']
    sort_var.sort(key = lambda x:x['createat'])
    for each in sort_var:
        time_tmp = float(each['createat'])
        each['createat'] = time.asctime(time.localtime(time_tmp))
        time_tmp = float(each['updateat'])
        each['updateat'] = time.asctime(time.localtime(time_tmp))
        for item in dict_:
            if item in each:
                continue
            else:
                each[item] = None
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