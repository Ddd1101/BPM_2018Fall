import web
import model
import json
import requests
import time

urls = (
    '/','Register',
    '/api/users','users',
    '/api/user','users',
    '/api/users/login','users_login',
    '/profiles','profiles',
    '/api/articles','article',
    '/api/articles/get','articles_get',
    '/api/comments','comment'
)

url = 'http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS'

class users:
    #register
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        res = model.do_user_register(req['user'])
        if res == "":
            return json.dumps({'id': res,'res':'error'})
        else:
            return res

    #修改需要全部数据一起修改
    #update
    def PUT(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req =json.loads(req_str)
        req_ = req['user']
        user_id = req_['id']
        whole_param_  = requests.get(url + '/User/' + user_id)
        whole_param = json.loads(whole_param_.text)
        whole_param.pop('type')
        for key in req_:
            whole_param[key] = req_[key]
        whole_param.pop('id')
        rt_raw = requests.put(url + '/User/' + user_id,json.dumps(whole_param))
        rt_tmp = json.loads(rt_raw.text)
        rt_tmp.pop('type')
        rt = json.dumps({'user':rt_tmp})

        return rt;

class users_login:
    #login
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        res = model.do_user_login(req['user'])
        print(res)
        if res == "":
            res = json.dumps({'errors':{'body':'user not exist or psw error'}})
            rt = res
        else :
            rt = json.dumps({'user':res})
        return rt

class article:
    #submit
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        #create_time_ = time.asctime( time.localtime(time.time()))
        create_time_ = time.time()
        update_time_ =create_time_
        addition ='{"createat":"' + str(create_time_) + '","updateat":"' + str(update_time_) + '"}'
        req = json.loads(req_str)
        req_ = req['article']
        req_.update(json.loads(addition))
        req_.update(req['user'])
        authorid = req_.pop('userId')
        req_.update({"authorid":authorid})
        res = model.do_article_submit(req_)

    def PUT(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_get = json.loads(req_str)
        req = req_get['user']
        req.update(req['atticle'])
        res = model.do_article_update(req)

    def DELETE(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_get = json.loads(req_str)
        req = req_get['article']
        res = model.do_article_delete(req)

    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_get = json.loads(req_str)
        print(req_get)

class articles_get:

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_get = json.loads(req_str)
        req = req_get['param']
        authorid = req.pop('userId')
        req.update({"authorid":authorid})
        print(req)
        rt = model.do_aticle_list(req)
        return rt

class comment:

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
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
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req_raw = json.loads(req_str)
        req = req_raw['comment']
        res = model.do_comment_delete(req)

    
app =web.application(urls, globals())

if __name__ == '__main__':
    app.run()