import web
import requests
from filter import DFAFilter

def post(src):
    content = src['content']

    gfw = DFAFilter()
    gfw.parse("keywords")
    gfw.filter(content, "*")

    src['content'] = content

    requests.post('http://119.23.241.119:8080/Entity/U3306a6d35762f/TNS/article', src)

