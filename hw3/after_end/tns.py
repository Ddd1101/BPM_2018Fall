import web
import model
import json
import requests
import time

urls = (
    '/', 'Register',
    '/api/users', 'users',
    '/api/users/get', 'user_get',
    '/api/user', 'users',
    '/api/users/login', 'users_login',
    '/api/profiles', 'profile',
    '/api/articles', 'article',
    '/api/articles/get', 'articles_get',
    '/api/articles/tag', 'tags',
    '/api/tags', 'taglist',
    '/api/comments', 'comment',
    '/api/chiefeditor/assign', 'chiefeditor',
    '/api/editor/register', 'editor_register',
    '/api/editor/get', 'editorlist',
    '/api/editor/login', 'editor',
    '/api/editor/register', 'editor_register',
    '/api/editor/reviewlist', 'editor',
    '/api/editor/review', 'review',
    '/api/editor/assignlist', 'assign',
    '/api/chiefeditor/editors', 'editorlist',
    '/delete', 'delete'
)

url = 'http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS'


class delete:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        list_raw = requests.get(url + '/Tag/')
        list = json.loads(list_raw.text)
        list = list['Tag']
        for each in list:
            requests.delete(url+'/Tag/'+str(each['id']))

class assign:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        rt = model.do_get_assign_list()
        return rt


class review:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        req = req['review']
        if req['editorid'] == 1544853927169:
            rt = model.do_review_supervisor(req)
        else:
            rt = model.do_review(req)
        return rt


class editor:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        rt = model.do_editor_login(req['editor'])
        return rt

    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_raw = web.input()
        if req_raw['editorid'] == str(1544853927169):
            rt = model.do_get_review_list()
        else:
            rt = model.do_get_review_list_1(req_raw['editorid'])
        return rt


class editorlist:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        rt = model.do_avaliable_editor()
        return rt


class editor_register:
    # register
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        rt = model.do_editor_register(req['editor'])
        return rt


class chiefeditor:
    # assign
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        res = model.do_assign(req['article'])
        return res


class users:

    # register
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        res = model.do_user_register(req['user'])
        if res == "":
            return json.dumps({'id': res, 'res': 'error'})
        else:
            return res

    # 修改需要全部数据一起修改
    # update
    def PUT(self):
        dict_ = ['email', 'id', 'username', 'bio', 'image']
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        req_ = req['user']
        user_id = req_['id']
        whole_param_ = requests.get(url + '/User/' + str(user_id))
        whole_param = json.loads(whole_param_.text)
        whole_param.pop('type')
        for key in req_:
            whole_param[key] = req_[key]
        whole_param.pop('id')
        rt_raw = requests.put(url + '/User/' + str(user_id), json.dumps(whole_param))
        rt_tmp = json.loads(rt_raw.text)
        rt_tmp.pop('type')
        for each in dict_:
            if each in rt_tmp:
                continue
            else:
                rt_tmp.update({each: None})
        rt = json.dumps({'user': rt_tmp})

        return rt;


class users_login:
    # login
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        res = model.do_user_login(req['user'])
        if res == "":
            res = json.dumps({'errors': {'body': 'user not exist or psw error'}})
            rt = res
        else:
            rt = json.dumps({'user': res})
        return rt


class user_get:
    def POST(self):

        dict_ = ['email', 'id', 'username', 'bio', 'image']
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        req = req_raw['user']
        rt_raw = requests.get(url + '/User/?User.id=' + str(req['id']))
        rt = json.loads(rt_raw.text)
        rt = rt['User'][0]
        for each in dict_:
            if each not in rt:
                rt.update({each: None})
        return json.dumps({'user': rt})


class profile:
    def POST(self):
        dict_ = ['email', 'id', 'username', 'bio', 'image']
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        rt = model.do_profile_get(req_raw)
        return json.dumps({'profile': rt})


class article:
    # submit
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        create_time_ = time.time()
        update_time_ = create_time_
        addition = '{"createat":"' + str(create_time_) + '","updateat":"' + str(update_time_) + '"}'
        req = json.loads(req_str)
        req_ = req['article']
        req_.update(json.loads(addition))
        req_.update(req['user'])
        authorid = req_.pop('id')
        req_.update({"authorid": authorid})
        rt = model.do_article_submit(req_)
        return rt

    # update
    def PUT(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        rt = model.do_article_update(req_raw['article'])
        return rt

    def DELETE(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_raw = web.input()
        req_state = url + '/Article/' + str(req_raw['articleid'])
        rt = requests.delete(req_state)
        return json.loads(rt.text)

    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_raw = web.input()
        rt = ''
        if 'articleid' in req_raw:
            id = req_raw.pop('articleid')
            req_raw.update({'id': id})
        if '*' in req_raw:
            rt = model.do_articles_all()
            return rt
        rt = model.do_articles_get(req_raw)
        return rt


class articles_get:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_get = json.loads(req_str)
        req = req_get['param']
        rt = model.do_aticle_list(req)
        return rt

    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_raw = web.input()
        rt = ''
        if '*' in req_raw:
            rt = model.do_articles_all()
            return rt
        rt = model.do_articles_get(req_raw)
        return rt


class tags:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_get = json.loads(req_str)
        req = req_get['article']['id']
        res_raw = requests.get(url + '/Article/' + str(req))
        return json.dumps(res_raw.text)

    def PUT(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        rt = model.do_article_get_by_tag(req_raw['article'])
        return rt

    def DELETE(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        req = req_raw['tag']
        if 'articleid' in req:
            rt = model.do_delete_tag_article(req)
        else:
            rt = model.do_delete_tag(req)
        return rt

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        req = req_raw['tag']
        rt = model.do_add_article_tag(req)


class taglist:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        rt = model.do_get_taglist()
        return rt


class comment:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        create_time_ = time.asctime(time.localtime(time.time()))
        addition = '{"createat":"' + create_time_ + '"}'
        req = req_raw['user']
        req.update(req_raw['article'].text)
        req.update(req_raw['body'].text)
        req.update(addition)
        res = model.do_comment_commit(req)

    def DELETE(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        web.header('Access-Control-Allow-Credentials', 'true')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        req = req_raw['comment']
        res = model.do_comment_delete(req)


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
