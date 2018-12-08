import web
import model
import json
import requests
import time

urls = (
    '/','Register',
    '/api/users','users',
    '/api/user','users',
    '/users/login','users_login',
    '/profiles','profiles',
    '/api/articles','article',
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
        print(req)
        res = model.do_user_register(req['user'])
        print(res)
        if res == "":
            return json.dumps({'id': res,'res':'error'})
        else:
            return json.dumps({'id': res, 'res': 'success'})

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
        whole_param_  = requests.get(url + 'User' + user_id)
        whole_param = json.loads(whole_param_)
        for key in req:
            whole_param[key] = req[key]
        requests.put(url + '/User/' + user_id,whole_param)

class users_login:
    #login
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        res = model.do_user_login(req)
        if res == "":
            res = json.dumps({"errors":{"body":["user not exist"]}})
        return res

class article:
    #submit
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        create_time_ = time.asctime( time.localtime(time.time()))
        update_time_ =create_time_
        addition ='{"createat":"' + create_time_ + '","updateat":"'+update_time_+'"}'
        req = json.loads(req_str)
        req_ = req['article']
        req_.update(json.loads(addition))
        req_.update(req['user'])
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