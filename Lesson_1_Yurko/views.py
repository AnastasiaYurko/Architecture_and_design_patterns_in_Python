from my_framework.templates import template_build


class Index:
    def __call__(self, request):
        return '200 OK', template_build('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', template_build('page.html', date=request.get('date', None))


class Contact:
    def __call__(self, request):
        return '200 OK', template_build('contact.html', date=request.get('date', None))
