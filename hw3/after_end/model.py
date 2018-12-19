import web
import requests
import json
import time
from filter import DFAFilter
import _thread

url = 'http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS'


def do_get_assign_list():
    article_list_raw = requests.get(url + '/Article/?Aticle.stat=assigning')
    author_list_raw = requests.get(url + '/User/')
    editor_article_list_raw = requests.get(url + '/Review/')
    article_list = json.loads(article_list_raw.text)
    if len(article_list) > 0:
        article_list = article_list['Article']
    else:
        article_list = []
    author_list = json.loads(author_list_raw.text)
    if len(author_list) > 0:
        author_list = author_list['User']
    else:
        author_list = []
    editor_article_list = json.loads(editor_article_list_raw.text)
    if len(editor_article_list) > 0:
        editor_article_list = editor_article_list['Review']
    else:
        editor_article_list = []
    rt_list = []
    for each in article_list:
        articleid = each['id']
        tmp = 0
        for item in editor_article_list:
            if articleid == item['articleid']:
                tmp += 1
        if tmp < 2:
            authorid = each['authorid']
            for item in author_list:
                if authorid == item['id']:
                    each.update({'author': item['username']})
            rt_list.append(each)
    return json.dumps({'statuscode': 200, 'assignlist': rt_list})


def do_get_taglist():
    res_raw = requests.get(url + '/Tag/')
    res = json.loads(res_raw.text)
    res = res['Tag']
    rt = []
    for each in res:
        rt.append(each["tag"])
    rt = json.dumps({"tags": rt})
    return rt


def do_add_article_tag(param):
    taglist = param['taglist']
    tag_list_raw = requests.get(url + '/Tag/')
    tag_list_json = json.loads(tag_list_raw)
    tag_article_list_raw = requests.get(url + '/Tag_article/?Tag_article.articleid=' + str(param['articleid']))
    tag_article_list_json = json.loads(tag_article_list_raw.text)
    if len(tag_article_list_json) > 0:
        tag_article_list_json = tag_article_list_json['Tag_article']
    else:
        tag_article_list_json = []
    tag_article_list = []
    for each in tag_article_list_json:
        tag_article_list.append(each['tag'])
    if len(tag_list_json) > 0:
        tag_list_json = tag_list_json['Tag']
    tag_list = []
    for each in tag_list_json:
        tag_list.append(each['tag'])
    for each in taglist:
        if each not in tag_list:
            requests.post(url + '/Tag/', json.dumps({'tag': each}))
        if each not in tag_article_list:
            requests.post(url + 'Tag_article', json.dumps({'tag': each, 'articleid': param['articleid']}))
    return json.dumps({'statuscode': 200})


def do_delete_tag(param):
    res_get_tagid_raw = requests.get(url + '/Tag/?Tag.tag=' + param['tag'])
    rag_get_tagid = json.load(res_get_tagid_raw.text)
    tagid = rag_get_tagid['Tag'][0]
    res_raw = requests.delete(url + '/Tag/' + tagid)
    return res_raw


def do_delete_tag_article(param):
    res_get_itemid_raw = requests.get(
        url + '/Tag_article/?Tag.tag=' + param['tag'] + '&Tag.articleid=' + param['articleid'])
    res_get_itemid = json.loads(res_get_itemid_raw.text)
    itemid = res_get_itemid['Tag_article'][0]
    rt_raw = requests.delete(url + '/Tag_article/' + itemid)
    if rt_raw.ok:
        return json.dumps({'success': {'statuscode': 200}})
    else:
        return json.dumps({'error': {'statuscode': 400, 'description': 'something wrong happen'}})


def do_review(param):
    dict_review = ['editorid', 'articleid', 'trust', 'remark', 'decision']
    res = requests.get(
        url + '/Review/?Review.editorid=' + str(param['editorid']) + '&Review.articleid=' + str(param['articleid']))
    res = json.loads(res.text)
    if len(res) == 0:
        res = requests.post(url + '/Review/', json.dumps(param))
        if res.ok:
            rt = json.dumps({'success': {'statuscode': 200}})
        else:
            rt = json.dumps({'error': {'statuscode': res.status_code}})
        return rt
    else:
        res = res['Review'][0]
        for each in dict_review:
            res[each] = param[each]
        reviewid = res.pop('id')
        res = requests.put(url + '/Review/' + str(reviewid), json.dumps(res))
        if res.ok:
            rt = json.dumps({'success': {'statuscode': 200}})
        else:
            rt = json.dumps({'error': {'statuscode': res.status_code}})
        return rt


def do_review_supervisor(param):
    dict_review = ['editorid', 'articleid', 'trust', 'remark', 'decision']
    res = requests.get(
        url + '/Supervisor_article/?Supervisor_article.editorid=' + str(
            param['editorid']) + '&Supervisor_article.articleid=' + str(param['articleid']))
    res = json.loads(res.text)
    res = res['Review'][0]
    for each in dict_review:
        res[each] = param[each]
    reviewid = res.pop('id')
    res = requests.put(url + '/Supervisor_article/' + str(reviewid), json.dumps(res))
    # change article status
    aritcle_info_raw = requests.get(url + '/Aricle/' + str(param['articleid']))
    article_info = json.loads(aritcle_info_raw.text)
    article_info.pop('type')
    article_info.update({'stat': param['decision']})
    articleid = article_info.pop('id')
    requests.put(url + '/Artilce/' + str(articleid), json.dumps(article_info))
    if res.ok:
        rt = json.dumps({'success': {'statuscode': 200}})
    else:
        rt = json.dumps({'error': {'statuscode': res.status_code}})
    return rt


# for supervisor
def do_get_review_list(param):
    # get all info needed
    article_list = requests.get(url + '/Article/')
    article_list = json.loads(article_list.text)
    article_list = article_list['Article']
    author_list = requests.get(url + '/User/')
    author_list = json.loads(author_list.text)
    author_list = author_list['User']
    articleid_list1 = requests.get(url + '/Review/?editorid=' + param)
    articleid_list1 = json.loads(articleid_list1.text)
    articleid_list1 = articleid_list1['Review']
    tag_article_list = requests.get(url + '/Tag_article/')
    tag_article_list = json.loads(tag_article_list.text)
    if len(tag_article_list) > 0:
        tag_article_list = tag_article_list['Tag_article']
    else:
        tag_article_list = []
    # pack articleid
    articleid_list = []
    for each in articleid_list1:
        articleid_list.append(each['articleid'])
    # pack rt article list
    rt_list = []
    for each in article_list:
        if each['id'] in articleid_list:
            taglist = []
            for item in tag_article_list:
                if str(each['id']) == str(item['articleid']):
                    taglist.append(item['tag'])
            each.update({'taglist': taglist})
            each.pop('createat')
            each.pop('updateat')
            review_raw = requests.get(url + '/Review/?Review.articleid=' + str(each['id']))
            review = json.loads(review_raw)
            supervisor_article_raw = requests.get(url + '/Supervisor_article/')
            supervisor_article_json = json.loads(supervisor_article_raw.text)
            if len(supervisor_article_json) > 0:
                supervisor_article_json = supervisor_article_json['Supervisor_article']
            else:
                supervisor_article_json = []
            supervisor_article = []
            for item in supervisor_article_json:
                supervisor_article.append(item['articleid'])
            if len(review) == 2:
                if (each['stat'] == 'checking') and (each['id'] not in supervisor_article):
                    rt_list.append(each)
    authorid_list = []
    for each in author_list:
        authorid_list.append(each['id'])
    for each in rt_list:
        if each['authorid'] in authorid_list:
            for item in author_list:
                if each['authorid'] == item['id']:
                    each.update({'author': item['username']})
            each.pop('authorid')
    rt = json.dumps({'statuscode': 200, 'reviewlist': rt_list})
    return rt


# for editor
def do_get_review_list_1(param):
    # get all info needed
    article_list = requests.get(url + '/Article/')
    article_list = json.loads(article_list.text)
    article_list = article_list['Article']
    author_list = requests.get(url + '/User/')
    author_list = json.loads(author_list.text)
    author_list = author_list['User']
    articleid_list1 = requests.get(url + '/Review/?editor1id=' + param)
    articleid_list1 = json.loads(articleid_list1.text)
    articleid_list1 = articleid_list1['Review']
    tag_article_list = requests.get(url + '/Tag_article/')
    tag_article_list = json.loads(tag_article_list.text)
    if len(tag_article_list) > 0:
        tag_article_list = tag_article_list['Tag_article']
    else:
        tag_article_list = []
    # pack articleid
    articleid_list = []
    for each in articleid_list1:
        articleid_list.append(each['articleid'])
    # pack rt article list
    rt_list = []
    for each in article_list:
        if each['id'] in articleid_list:
            taglist = []
            for item in tag_article_list:
                if str(each['id']) == str(item['articleid']):
                    taglist.append(item['tag'])
            each.update({'taglist': taglist})
            each.pop('createat')
            each.pop('updateat')
            if each['stat'] == 'checking':
                rt_list.append(each)
    authorid_list = []
    for each in author_list:
        authorid_list.append(each['id'])
    for each in rt_list:
        if each['authorid'] in authorid_list:
            for item in author_list:
                if each['authorid'] == item['id']:
                    each.update({'author': item['username']})
            each.pop('authorid')

    rt = json.dumps({'statuscode': 200, 'reviewlist': rt_list})
    return rt


def do_avaliable_editor():
    res_raw = requests.get(url + '/Editor/')
    res = json.loads(res_raw.text)
    res_raw = res['Editor']
    rt = {'editors': None}
    rt_ = []
    res = []
    for each in res_raw:
        if each['id'] != 1544853927169:
            res.append(each)
    print(res)
    for each in res:
        if 'maxreview' in each:
            if each['maxreview'] < 30:
                # each.pop('eamil')
                each.pop('password')
                each.pop('maxreview')
                rt_.append(each)
    rt = json.dumps({'statuscode': 200, 'editors': rt_})
    return rt


def do_editor_login(param):
    res_raw = requests.get(url + '/Editor/?Editor.editorname=' + param['editorname'])
    res = json.loads(res_raw.text)
    if len(res) == 0:
        rt = json.dumps({'error': {'statuscode': 400, 'description': 'no such editorname'}})
        return rt
    else:
        rt = res['Editor'][0]
        if rt['password'] != param['password']:
            rt = json.dumps({'error': {'statuscode': 400, 'description': 'pwd error'}})
            return rt
        else:
            rt.pop('password')
            if 'maxreview' in rt:
                rt.pop('maxreview')
            return json.dumps({'statuscode': 200, 'editor': rt})


def do_editor_register(param):
    res = requests.post(url + '/Editor/', json.dumps(param))
    if res.ok:
        rt = json.dumps({'success': {'statuscode': 200}})
        return rt
    else:
        rt = json.dumps({'error': {'statuscode': res.status_code}})
        return rt


def do_assign(param):
    # editorname->id
    res1_raw = requests.get(url + '/Editor/?Editor.editorname=' + param['editor1name'])
    res1 = json.loads(res1_raw.text)
    param.pop('editor1name')
    param.update({'editor1id': res1["Editor"][0]["id"]})
    res2_raw = requests.get(url + '/Editor/?Editor.editorname=' + param['editor2name'])
    res2 = json.loads(res2_raw.text)
    param.pop('editor2name')
    param.update({'editor2id': res1["Editor"][0]["id"]})
    #
    to_remark = {'articleid': param['articleid'], 'editorid': param['editor1id'], 'decision': 'checking'}
    res_tmp = requests.post(url + '/Review/', json.dumps(to_remark))
    to_remark = {'articleid': param['articleid'], 'editorid': param['editor2id'], 'decision': 'checking'}
    res_tmp = requests.post(url + '/Review/', json.dumps(to_remark))
    # article
    article_res_raw = requests.get(url + '/Article/' + str(param['articleid']))
    article_res = json.loads(article_res_raw.text)
    article_res.pop('type')
    article_res.update({'stat': 'checking'})
    article_res.pop('id')
    article_rt = requests.put(url + '/Article/' + str(param['articleid']), json.dumps(article_res))
    # num of review ++
    dict_editor = ['id', 'email', 'editorname', 'password', 'maxreview']
    editor1_info_raw = requests.get(url + '/Editor/' + str(param['editor1id']))
    editor1_info = json.loads(editor1_info_raw.text)
    editor1_info.pop('type')
    if 'maxreview' in editor1_info:
        editor1_info['maxreview'] = editor1_info['maxreview'] + 1
    else:
        editor1_info.update({'maxreview': 1})
    editor1_info.pop('id')
    requests.put(url + '/Editor/' + str(param['editor1id']), json.dumps(editor1_info))
    editor2_info_raw = requests.get(url + '/Editor/' + str(param['editor2id']))
    editor2_info = json.loads(editor2_info_raw.text)
    editor2_info.pop('type')
    # change article status
    stat_res = chang_article_stat(param['articleid'], 'checking')
    if 'maxreview' in editor2_info:
        editor2_info['maxreview'] = editor2_info['maxreview'] + 1
    else:
        editor2_info.update({'maxreview': 1})
    editor2_info.pop('id')
    res = requests.put(url + '/Editor/' + str(param['editor2id']), json.dumps(editor2_info))
    if res.ok:
        rt = json.dumps({'success': {'statuscode': 200}})
        return rt
    else:
        rt = json.dumps({'error': {'statuscode': res.status_code}})
        return rt


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
    tag_list_raw = requests.get(url + '/Tag/')
    tag_list_json = json.loads(tag_list_raw.text)
    if len(tag_list_json) > 0:
        tag_list_json = tag_list_json['Tag']
    else:
        tag_list_json = []
    tag_list = []
    for each in tag_list_json:
        tag_list.append(each['tag'])

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
    requests.post(url + '/Supervisor_article/', json.dumps({'supervisorid': 1544853927169, 'articleid': articleid}))
    stat_res = chang_article_stat(articleid, 'assigning')

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
            rt = requests.post(url + '/Tag_article/', json.dumps(param_tag_article))
            if key not in tag_list:
                requests.post(url + '/Tag/', json.dumps({'tag': key}))
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
    rt['updateat'] = time.asctime(time.localtime(float(time.time())))
    return json.dumps({'article': rt})


def do_article_delete(param):
    res = requests.delete(url + '/Article/' + str(param['id']))
    res = json.loads(res.text)
    return res


def do_articles_get(param):
    if 'tag' in param:
        return do_article_get_by_tag(param)
    dict_ = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'stat', 'author', 'taglist', 'editor']
    dict_author = ['email', 'id', 'username', 'bio', 'image']
    dict_supervisor = ['id', 'decision', 'remark']
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


def do_article_get_by_tag(param):
    dict_article = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'stat', 'author', 'taglist',
                    'editor']
    dict_author = ['email', 'id', 'username', 'bio', 'image']
    dict_supervisor = ['id', 'status', 'remark']
    dict_editor = ['id', 'decision', 'trust', 'remark']
    # get all list
    tag_article_list_raw = requests.get(url + '/Tag_article/')
    tag_article_list = json.loads(tag_article_list_raw.text)
    if len(tag_article_list) > 0:
        tag_article_list = tag_article_list['Tag_article']
    else:
        tag_article_list = []
    article_list_raw = requests.get(url + '/Article/')
    article_list = json.loads(article_list_raw.text)
    if len(article_list) > 0:
        article_list = article_list['Article']
    else:
        article_list = []
    author_list_raw = requests.get(url + '/User/')
    author_list = json.loads(author_list_raw.text)
    if len(author_list) > 0:
        author_list = author_list['User']
    else:
        author_list = []
    supervisor_list_raw = requests.get(url + '/Supervisor_article/')
    supervisor_list = json.loads(supervisor_list_raw.text)
    if len(supervisor_list) > 0:
        supervisor_list = supervisor_list['Supervisor_article']
    else:
        supervisor_list = []
    editor_list_raw = requests.get(url + '/Editor_article/')
    editor_list = json.loads(editor_list_raw.text)
    if len(editor_list) > 0:
        editor_list = editor_list['Editor_article']
    else:
        editor_list = []
    tag_list_raw = requests.get(url + '/Tag_article/')
    tag_list = json.loads(tag_list_raw.text)
    if len(tag_list) > 0:
        tag_list = tag_list['Tag_article']
    else:
        tag_list = []
    # find by tag
    taget_tag = param['tag']
    articleid_list = []
    for each in tag_article_list:
        if each['tag'] == taget_tag:
            articleid_list.append(int(each['articleid']))
    rt_article_list = []
    for each in article_list:
        if each['id'] in articleid_list:
            # full fill article items
            for item_of_article_dict in dict_article:
                if item_of_article_dict not in each:
                    each[item_of_article_dict] = None
            each.update({'editor': {'supervisor': None, 'editor1': None, 'editor2': None}})
            each.update({'status': 'checking'})
            # taglist
            taglist = []
            for item in tag_list:
                if item['articleid'] == str(each['id']):
                    taglist.append(item['tag'])
                if len(taglist) > 0:
                    each.update({'taglist': taglist})
            if len(taglist) > 0:
                each['taglist'] = taglist
            # time
            time_tmp = float(each['createat'])
            each['createat'] = time.asctime(time.localtime(time_tmp))
            time_tmp = float(each['updateat'])
            each['updateat'] = time.asctime(time.localtime(time_tmp))
            # editor
            it = 1
            for item in editor_list:
                if item['articleid'] == each['id']:
                    for itor in dict_editor:
                        if itor not in item:
                            item.update({itor: None})
                    item.pop('articleid')
                    each['editor'].update({('editor' + it): item})
                    it += 1
            # supervisor
            for item in supervisor_list:
                if item['articleid'] == each['id']:
                    for itor in dict_supervisor:
                        if itor not in item:
                            item.update({itor: None})
                    item.pop('articleid')
                    each['editor'].update({'supervisor': item})
            # author
            for item in author_list:
                if item['id'] == each['authorid']:
                    for itor in dict_author:
                        if itor not in item:
                            item.update({itor: None})
                    if 'password' in item:
                        item.pop('password')
                    each.update({'author': item})
            each.pop('authorid')
            rt_article_list.append(each)
    rt = json.dumps({'articles': rt_article_list})
    rt = json.loads(rt)
    rt.update({'articlescount': len(rt_article_list)})
    return json.dumps(rt)


def do_article_status(articleid):
    return 0


def do_add_tag_to_article(param):
    req = param['article']
    articleid = 0
    if 'articleid' in req:
        articleid = req['articleid']
    elif 'id' in req:
        articleid = req['id']
    taglist = param['taglist']
    for each in taglist:
        param_ = json.dumps({'tag': each, 'articleid': articleid})
        requests.post(url + '/Tag_article/', )
    req_state = json.dumps({'id': articleid})
    rt = do_articles_get(req_state)
    return rt


def do_articles_all():
    dict_article = ['id', 'title', 'description', 'body', 'createat', 'updateat', 'stat', 'author', 'taglist',
                    'editor']
    dict_author = ['email', 'id', 'username', 'bio', 'image']
    dict_supervisor = ['id', 'status', 'remark']
    dict_editor = ['id', 'decision', 'trust', 'remark']
    # get all resource
    articles_res_raw = requests.get(url + '/Article/')
    supervisor_res_raw = requests.get(url + '/Supervisor_article/')
    editor_res_raw = requests.get(url + '/Review/')
    author_res_raw = requests.get(url + '/User/')
    tag_res_raw = requests.get(url + '/Tag_article/')
    articles_info = json.loads(articles_res_raw.text)
    if len(articles_info) > 0:
        articles_info = articles_info['Article']
    else:
        articles_info = []
    supervisor_info = json.loads(supervisor_res_raw.text)
    if len(supervisor_info) > 0:
        supervisor_info = supervisor_info['Supervisor_article']
    else:
        supervisor_info = []
    editor_info = json.loads(editor_res_raw.text)
    if len(editor_info) > 0:
        editor_info = editor_info['Review']
    else:
        editor_info = []
    author_info = json.loads(author_res_raw.text)
    if len(author_info) > 0:
        author_info = author_info['User']
    else:
        author_info = []
    tag_info = json.loads(tag_res_raw.text)
    if len(tag_info) > 0:
        tag_info = tag_info['Tag_article']
    else:
        tag_info = []
    # pack article list
    for each in articles_info:
        # full fill article items
        for item_of_article_dict in dict_article:
            if item_of_article_dict not in each:
                each[item_of_article_dict] = None
        each.update({'editor': {'supervisor': None, 'editor1': None, 'editor2': None}})
        each.update({'status': 'checking'})
        # taglist
        taglist = []
        for item in tag_info:
            if item['articleid'] == str(each['id']):
                taglist.append(item['tag'])
            if len(taglist) > 0:
                each.update({'taglist': taglist})
        if len(taglist) > 0:
            each['taglist'] = taglist
        # time
        time_tmp = float(each['createat'])
        each['createat'] = time.asctime(time.localtime(time_tmp))
        time_tmp = float(each['updateat'])
        each['updateat'] = time.asctime(time.localtime(time_tmp))
        # editor
        it = 1
        for item in editor_info:
            if item['articleid'] == each['id']:
                for itor in dict_editor:
                    if itor not in item:
                        item.update({itor: None})
                each['editor'].update({('editor' + str(it)): item})
                it += 1
        # supervisor
        for item in supervisor_info:
            if item['articleid'] == each['id']:
                for itor in dict_supervisor:
                    if itor not in item:
                        item.update({itor: None})
                each['editor'].update({'supervisor': item})
        # author
        for item in author_info:
            if item['id'] == each['authorid']:
                for itor in dict_author:
                    if itor not in item:
                        item.update({itor: None})
                if 'password' in item:
                    item.pop('password')
                each.update({'author': item})
        each.pop('authorid')
    rt = json.dumps({'articles': articles_info})
    rt = json.loads(rt)
    rt.update({'articlescount': len(articles_info)})
    return json.dumps(rt)


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


def chang_article_stat(articleid, stat):
    article_res_raw = requests.get(url + '/Article/' + str(articleid))
    article_res = json.loads(article_res_raw.text)
    article_res.pop('type')
    article_res.update({'stat': stat})
    article_res.pop('id')
    rt = requests.put(url + '/Article/' + str(articleid), article_res)
    return rt.status_code
