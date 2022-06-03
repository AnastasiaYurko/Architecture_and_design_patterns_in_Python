from my_framework.core import MyFramework
from my_framework.routes import routes, fronts
from wsgiref.simple_server import make_server


app = MyFramework(routes, fronts)

with make_server('', 8000, app) as httpd:
    print("Запуск порта 8000...")
    httpd.serve_forever()
    