import datetime
import os.path

from my_framework.templates import template_build


class Index:
    def __call__(self, request):
        return '200 OK', template_build('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', template_build('page.html', date=request.get('date', None))


class Contact:
    def __call__(self, request):
        if request['request_method'] == 'POST':
            now = datetime.datetime.now()
            data = request['data']
            title = data['title']
            text = data['text']
            email = data['email']

            if not os.path.exists('messages'):
                os.mkdir('messages')

            with open(f'messages/message_{now.strftime("%d%m%Y")}_{now.strftime("%H%M%S")}.txt', 'w',
                      encoding='utf-8') as message:
                message.write(f'Нам пришло сообщение от {now.strftime("%d.%m.%Y")} в {now.strftime("%H:%M:%S")}!\n'
                              f'Отправитель: {email}\n'
                              f'Тема: {title}\n'
                              f'Текст: {text}')
            return '200 OK', template_build('contact.html', date=request.get('date', None))

        else:
            return '200 OK', template_build('contact.html', date=request.get('date', None))
