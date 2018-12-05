import web
import model
import json

urls = (
    '/','REgister',
    '/article_filter', 'article_filter',
    '/comment_filter','comment_filter',
    '/register/','Register',
    '/login','login',
)

#web.header("Access-Control-Allow-Origin", "*")
#web.header('content-type', 'application/json')

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

class Register:

    def Post(self):
        print("get in register_post")
        #return json.dumps({'res': 'post'})
        #web.header("Access-Control-Allow-Origin", "*")
        #web.header('content-type', 'application/json')
        #print("get in register_post")
        req = web.input()
        #res = model.do_register(req)
        #return json.dumps({'res':res})

    def Get(self):
        return json.dump({'res':'get'})
class login:

    def Get(self):
        req = web.input()


app =web.application(urls, globals())

if __name__ == '__main__':
    app.run()