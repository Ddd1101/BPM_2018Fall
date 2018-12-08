import web
import model
import json
import requests
import time

urls = (
    '/','Register',
    '/users','users',
    '/users/login','users_login',
    '/profiles','profiles',
    '/article','article',
    '/article_filter', 'article_filter',
    '/comment_filter','comment_filter'
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
        res = model.do_user_register(req)
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
        user_id = req['id']
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
        req.update(json.loads(addition))
        res = model.do_article_submit(req)


class comment_filter:

    def Post(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req = web.input()
        model.do_comment_filter(req)


app =web.application(urls, globals())

if __name__ == '__main__':
    app.run()