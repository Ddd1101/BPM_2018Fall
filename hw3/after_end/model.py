import web
import requests
import json
import time
from filter import DFAFilter

url = 'http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS'


def do_user_register(param):
    dict_ = ['email', 'id', 'username', 'bio', 'image']
    name = param['username']
    email = param['email']
    res_name = requests.get(url + '/User/?User.username=' + name)
    json_name = json.loads(res_name.text)
    res_email = requests.get(url + '/User/?User.email=' + email)
    json_email = json.loads(res_email.text)
    rt = ""
    if len(json_name) == 0 and len(json_email) == 0:
        if 'inmage' not in param:
            param.update({
                'image': 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2588767485,2358347029&fm=26&gp=0.jpg'})
        _param = json.dumps(param)
        tmp = requests.post(url + '/User/', _param)
        rt_raw = json.loads(tmp.text)
        rt_raw.pop("type")
        for each in dict_:
            if each in rt_raw:
                continue
            else:
                rt_raw.update({each: None})
        rt = json.dumps({'user': rt_raw})
        return rt
    else:
        return rt


def do_user_login(param):
    dict_ = ['email', 'id', 'username', 'bio', 'image']
    name = param['username']
    res = requests.get(url + '/User/?User.username=' + name)
    rt_raw = json.loads(res.text)
    rt = ""
    if len(rt_raw) != 0:
        pwd = rt_raw['User'][0].pop('password')
        if param['password'] != pwd:
            return rt
        else:
            rt = rt_raw['User'][0]
            for each in dict_:
                if each in rt:
                    continue
                else:
                    rt.update({each: None})
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
    rt = res_2['User'][0]
    rt.pop('password')
    for each in dict_:
        if each not in rt:
            rt.update({each: None})
    res_follow = json.loads(res_raw_follow.text)
    if len(res_follow) > 0:
        res_follow = res_follow['Follow']
        if len(res_follow) > 0:
            rt.update({'follow': True})
        else:
            rt.update({'follow': False})
    else:
        rt.update({'follow': False})
    return rt


# 2018/12/10 9.16am add taglist module by:gxhou
def do_article_submit(param):
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'status', 'authorid']
    content = param['title']
    gfw = DFAFilter()
    # gfw.parse("keywords")
    # res = gfw.filter(content, "*")
    # param['title'] = res

    content = param['description']
    # res = gfw.filter(content, "*")
    # param['description'] = res

    content = param['body']
    # res = gfw.filter(content, "*")
    # param['body'] = res

    has_tag = False
    taglist = ""
    if 'taglist' in param:
        has_tag = True
        taglist = param.pop('taglist')
    _param = json.dumps(param)
    response_1 = requests.post(url + '/Article/', _param)
    response_1 = json.loads(response_1.text)
    response_1.pop('type')
    articleid = response_1.pop('id')

    for each in dict_:
        if each in response_1:
            continue
        else:
            response_1[each] = None

    time_tmp = float(response_1['createat'])
    response_1['createat'] = time.asctime(time.localtime(time_tmp))
    time_tmp = float(response_1['updateat'])
    response_1['updateat'] = time.asctime(time.localtime(time_tmp))

    response_1.update({'articleid': articleid})
    if has_tag == True:
        for key in taglist:
            param_tag_article = json.dumps({'articleid': articleid})
            param_tag_article = json.loads(param_tag_article)
            param_tag_article.update({'tag': key})
            print(url + '/Tag_article/', json.dumps(param_tag_article))
            rt = requests.post(url + '/Tag_article/', json.dumps(param_tag_article))
            print(rt)
        response_2 = json.dumps(response_1)
        response_2 = json.loads(response_2)
        response_2.update({'taglist': taglist})
        return json.dumps({'article': response_2})
    else:
        return json.dumps({'article': response_1})


def do_article_update(param):
    req_state = url + '/Article/' + str(param.pop('id'))
    time_tmp = time.time()
    param.update({'updateat': str(time_tmp)})
    get_src = requests.get(req_state)
    get_src = json.loads(get_src.text)
    get_src.pop('type')
    for key in param:
        get_src[key] = param[key]
    rt_raw = requests.put(req_state, json.dumps(get_src))
    rt = json.loads(rt_raw.text)
    rt.pop('type')
    rt['createat'] = time.asctime(time.localtime(float(rt['createat'])))
    rt['updateat'] = time.asctime(time.localtime(float(rt['updateat'])))
    return json.dumps({'article': rt})


def do_article_delete(param):
    res = requests.delete(url + '/Article/' + str(param['id']))
    res = json.loads(res.text)
    return res


def do_articles_get(param):
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'status', 'author', 'taglist', 'editor']
    dict_author = ['email', 'id', 'username', 'bio', 'image']
    dict_supervisor = ['id', 'status', 'remark']
    dict_editor = ['id', 'status', 'trust', 'remark']
    req_state = url + '/Article/'
    it = 0
    if 'articleid' in param:
        id_tmp = param.pop('articleid')
        param.update({'id': id_tmp})
    if 'username' in param:
        username = param.pop('username')
        author_info_raw = requests.get(url + '/User/?User.username=' + username)
        author_info = json.loads(author_info_raw.text)
        param['authorid'] = str(author_info['User'][0]['id'])
    for each in param:
        if it == 0:
            req_state += ('?Article.' + each + '=' + param[each])
            it += 1
        else:
            req_state += ('&Article.' + each + '=' + param[each])
    rt_raw = requests.get(req_state)
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
        # each.pop('type')
        # item_time
        time_tmp = float(each['createat'])
        each['createat'] = time.asctime(time.localtime(time_tmp))
        time_tmp = float(each['updateat'])
        each['updateat'] = time.asctime(time.localtime(time_tmp))
        # item author
        authorid = each['authorid']
        author_info_res = requests.get(url + '/User/' + str(authorid))
        each.pop('authorid')
        author_info = json.loads(author_info_res.text)
        author_info.pop('password')
        author_info.pop('type')
        for itor in dict_author:
            if itor not in author_info:
                author_info.update({itor: None})
        each.update({'author': author_info})
        # item supervisor
        each.update({'editor': None})
        supervisor_info_res = requests.get(url + '/Supervisor_article/?Supervisor_article.articleid=' + str(each['id']))
        supervisor_info = json.loads(supervisor_info_res.text)
        if len(supervisor_info) == 0:
            each['editor'] = json.dumps({'supervisor': None})
        else:
            supervisor_info = supervisor_info['Supervisor_article'][0]
            for itor in dict_supervisor:
                if itor not in supervisor_info:
                    supervisor_info.update({itor: None})
                    each['editor'] = json.dumps({'supervisor': supervisor_info})
        # item editor
        editor_info_res = requests.get(url + '/Editor_article/?articleid=' + str(each['id']))
        editor_info = json.loads(editor_info_res.text)
        each['editor'] = json.loads(each['editor'])
        item_editor = each['editor']
        item_editor.update({'editor1': None})
        item_editor.update({'editor2': None})
        if len(editor_info) != 0:
            it = 1
            for itor in editor_info['Editor_article']:
                for item in dict_editor:
                    if item not in itor:
                        itor.update({item: None})
                        if itor == 'decision':
                            itor.update({item: 'checking'})
                each['editor'].update({('editor' + it): itor})
                it += 1
        # item status
        if 'status' not in each:
            each.update({'status': False})
        else:
            if each['status'] == 'True':
                each['status'] = True
            else:
                each['status'] = False
        for item in dict_:
            if item not in each:
                each[item] = None
        # item tag
        tag_info_res = requests.get(url + '/Tag_article/?Tag_article.articleid=' + str(each['id']))
        tag_info = json.loads(tag_info_res.text)
        if len(tag_info) == 0:
            each.update({'taglist': None})
        else:
            taglist = {}
            for itor in tag_info:
                tag_info = json.dumps(tag_info[itor])
                tag_info = json.loads(tag_info)
                tag_dict = []
                for i in tag_info:
                    tag_dict.append(i.pop('tag'))
                each.update({'taglist': tag_dict})
    res = json.dumps(res)
    return res


def do_articles_all():
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'status', 'author', 'taglist', 'editor']
    dict_author = ['email', 'id', 'username', 'bio', 'image']
    dict_supervisor = ['id', 'status', 'remark']
    dict_editor = ['id', 'status', 'trust', 'remark']
    req_state = url + '/Article/'
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
        # item time
        time_tmp = float(each['createat'])
        each['createat'] = time.asctime(time.localtime(time_tmp))
        time_tmp = float(each['updateat'])
        each['updateat'] = time.asctime(time.localtime(time_tmp))
        # item author
        authorid = each['authorid']
        author_info_res = requests.get(url + '/User/' + str(authorid))
        each.pop('authorid')
        author_info = json.loads(author_info_res.text)
        if 'password' in author_info:
            author_info.pop('password')
        if 'type' in author_info:
            author_info.pop('type')
        for itor in dict_author:
            if itor not in author_info:
                author_info.update({itor: None})
        each.update({'author': author_info})
        # item supervisor
        each.update({'editor': None})
        supervisor_info_res = requests.get(url + '/Supervisor_article/?Supervisor_article.articleid=' + str(each['id']))
        supervisor_info = json.loads(supervisor_info_res.text)
        if len(supervisor_info) == 0:
            each['editor'] = json.dumps({'supervisor': None})
        else:
            supervisor_info = supervisor_info['Supervisor_article'][0]
            for itor in dict_supervisor:
                if itor not in supervisor_info:
                    supervisor_info.update({itor: None})
                    each['editor'] = json.dumps({'supervisor': supervisor_info})
        # item editor
        editor_info_res = requests.get(url + '/Editor_article/?articleid=' + str(each['id']))
        editor_info = json.loads(editor_info_res.text)
        each['editor'] = json.loads(each['editor'])
        item_editor = each['editor']
        item_editor.update({'editor1': None})
        item_editor.update({'editor2': None})
        if len(editor_info) != 0:
            it = 1
            for itor in editor_info['Editor_article']:
                for item in dict_editor:
                    if item not in itor:
                        itor.update({item: None})
                        if itor == 'decision':
                            itor.update({item: 'checking'})
                each['editor'].update({('editor' + it): itor})
                it += 1
        # item status
        if 'status' not in each:
            each.update({'status': False})
        else:
            if each['status'] == 'True':
                each['status'] = True
            else:
                each['status'] = False
        for item in dict_:
            if item not in each:
                each[item] = None
        # item tag
        tag_info_res = requests.get(url + '/Tag_article/?Tag_article.articleid=' + str(each['id']))
        tag_info = json.loads(tag_info_res.text)
        if len(tag_info) == 0:
            each.update({'taglist': None})
        else:
            taglist = {}
            for itor in tag_info:
                tag_info = json.dumps(tag_info[itor])
                tag_info = json.loads(tag_info)
                tag_dict = []
                for i in tag_info:
                    tag_dict.append(i.pop('tag'))
                each.update({'taglist': tag_dict})
    res = json.dumps(res)
    return res


def do_aticle_list(param):
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'passstate', 'authorid']
    req_state = url + "/Article/"
    it = 0

    for key in param:
        if it == 0:
            req_state = req_state + "?Article." + key + "=" + param[key]
            it = it + 1
        else:
            req_state = req_state + "&Article." + key + "=" + param[key]
    res_raw = requests.get(req_state)
    res = json.loads(res_raw.text)
    print(res)
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


def do_comment_commit(param):
    content = param['body']
    gfw = DFAFilter()
    gfw.parse("keywords")
    gfw.filter(content, "*")

    param['body'] = content

    res = requests.post(url + '/comment', param)


def do_comment_delete(param):
    res = requests.delete(url + '/Comment/' + str(param['id']))
