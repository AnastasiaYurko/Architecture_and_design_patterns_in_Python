import os
from datetime import datetime

from my_framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data_month=request.get('data_month', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', data=request.get('data', None))


class Input:
    def __call__(self, request):
        return '200 OK', render('input.html', data=request.get('data', None))


class Editor:
    def __call__(self, request):
        return '200 OK', render('editor.html', objects_list=site.categories)


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Contacts:

    def __call__(self, request):
        if request['method'] == 'POST':
            now = datetime.now()
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
            return '200 OK', render('contact.html', date=request.get('date', None))

        else:
            return '200 OK', render('contact.html', date=request.get('date', None))


class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            type_ = data['type_']
            type_ = site.decode_value(type_)
            teacher = data['teacher']
            teacher = site.decode_value(teacher)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course(type_, name, category, teacher)
                site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            print(request)
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            return '200 OK', render('editor.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


class AddTeacher:

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            firstname = data['firstname']
            firstname = site.decode_value(firstname)
            teachers = None
            lastname = data['lastname']
            lastname = site.decode_value(lastname)
            user = site.create_user('teacher', firstname, lastname)
            site.teachers.append(user)

            return '200 OK', render('course_list.html', objects_list=teachers.user,
                                    firstname=teachers.firstname, lastname=teachers.lastname)
