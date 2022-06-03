class MyFramework:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, env, start_response):

        path = env['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes:
            view = self.routes[path]
            request = {}
            for controller in self.fronts:
                controller(request)
            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 PAGE NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Page not found!"]
