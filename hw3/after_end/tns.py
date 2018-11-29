import web
import model

urls = (
    '/', 'Filter'
)

class Filter:

    def post(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header('content-type', 'application/json')
        req = web.input()
        model.post(req)

app =web.application(urls, globals())

if __name__ == '__main__':
    app.run()