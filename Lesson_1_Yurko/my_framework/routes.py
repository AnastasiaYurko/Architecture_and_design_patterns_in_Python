from datetime import datetime
from views import Index, About, Contact


def date(request):
    request['date'] = datetime.today()


def other_front(request):
    request['key'] = 'key'


fronts = [date, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
}
