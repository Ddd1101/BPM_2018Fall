import web
import model
import json

urls = (
    '/','Register',
    '/article_filter', 'article_filter',
    '/comment_filter','comment_filter',
    '/api/user','Register',
    '/login','login',
)

#web.header("Access-Control-Allow-Origin", "*")
#web.header('content-type', 'application/json')

class Register:

    def POST(self):
        #return json.dumps({'res': 'post'})
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        #print("get in register_post")
        req_ = web.data()
        print(req_)
        req__ = str(req_, encoding="utf-8")
        print(req__)
        req = json.loads(req__)
        res = model.do_register(req)
        print(res)
        if res == "":
            return json.dumps({'id': res,'res':'error'})
        else:
            return json.dumps({'id': res, 'res': 'success'})


    def GET(self):
        return json.dumps({'res':'get'})

class article_filter:

    def POST(self):
        req = web.input()
        model.do_article_filter(req)

class comment_filter:

    def Post(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req = web.input()
        model.do_comment_filter(req)

class login:

    def Get(self):
        req = web.input()


app =web.application(urls, globals())

if __name__ == '__main__':
    app.run()