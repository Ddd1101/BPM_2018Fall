import web
import model
import json
import requests

urls = (
    '/','Register',
    '/users','users',
    '/users/login','users_login',
    '/article','article',
    '/article_filter', 'article_filter',
    '/comment_filter','comment_filter',
    '/login','login',
)

#web.header("Access-Control-Allow-Origin", "*")
#web.header('content-type', 'application/json')

url = 'http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS'

class users:

    def POST(self):
        #return json.dumps({'res': 'post'})
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        #print("get in register_post")
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
        res = model.do_user_register(req)
        if res == "":
            return json.dumps({'id': res,'res':'error'})
        else:
            return json.dumps({'id': res, 'res': 'success'})

    def PUT(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        print(req_bytes)
        req_str = str(req_bytes, encoding="utf-8")
        print(req_str)
        req =json.loads(req_str)
        print(req)
        user_id = req['id']
        param = req.pop('id')
        print(req)
        res = requests.put(url + '/User/' + user_id,param)
        print(res)


class users_login:

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        print(req_bytes)
        req_str = str(req_bytes, encoding="utf-8")
        print(req_str)
        req = json.loads(req_str)
        print("------->"+req)
        res = model.do_user_login(req)
        if res == "":
            res = json.dumps({"errors":{"body":["user not exist"]}})
        return res

class article:

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req_bytes = web.data()
        req_str = str(req_bytes, encoding="utf-8")
        req = json.loads(req_str)
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