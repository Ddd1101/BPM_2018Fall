import web
import model
import json

urls = (
    '/article_filter', 'article_filter'
    '/comment_filter','comment_filter'
    '/register','register'
    '/login','login'
)

#web.header("Access-Control-Allow-Origin", "*")
#web.header('content-type', 'application/json')

class article_filter:

    def POST(self):
        req = web.input()
        model.do_article_filter(req)

class comment_filter:

    def Post(self):
        req = web.input()
        model.do_comment_filter(req)

class register:

    def Post(self):
        req = web.input()
        res = model.do_register(req)
        return json.dumps({'res':res})

class login:

    def Get(self):
        req = web.input()


app =web.application(urls, globals())

if __name__ == '__main__':
    app.run()