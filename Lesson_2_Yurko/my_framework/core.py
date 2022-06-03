from quopri import decodestring
from my_framework.my_requests import PostRequests, GetRequests


class MyFramework:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, env, start_response):

        path = env['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        request_method = env['REQUEST_METHOD']
        request['request_method'] = request_method

        if request_method == 'POST':
            data = PostRequests().get_request_params(env)
            request['data'] = self.decode_data(data)
            print(f'Получен post-запрос: {self.decode_data(data)}')
        if request_method == 'GET':
            request_params = GetRequests().get_request_params(env)
            request['request_params'] = self.decode_data(request_params)
            print(f'Получены GET-параметры: {self.decode_data(request_params)}')

        if path in self.routes:
            view = self.routes[path]

            for controller in self.fronts:
                controller(request)
            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 PAGE NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Page not found!"]

    @staticmethod
    def decode_data(data):
        decoded_data = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            decoded_data[key] = val_decode_str
        return decoded_data
