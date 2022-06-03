from datetime import date


def secret_front(request):
    request['date'] = date.today()


def month_front(request):
    month_dict = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
                  9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
    i = date.today().month
    request['data_month'] = month_dict[i]


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front, month_front]
