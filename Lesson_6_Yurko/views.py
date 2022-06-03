import os
from my_framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from datetime import datetime
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    TemplateView, ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', data_month=request.get('data_month', None))


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html',  data=request.get('data', None))


@AppRoute(routes=routes, url='/input/')
class Input:
    @Debug(name='Input')
    def __call__(self, request):
        return '200 OK', render('input.html',  data=request.get('data', None))


@AppRoute(routes=routes, url='/editor/')
class Editor:
    def __call__(self, request):
        return '200 OK', render('editor.html', objects_list=site.categories)


class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/contacts/')
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


@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            course_type = data['course_type']
            course_info = data['course_info']
            course_teacher = data['course_teacher']
            name = site.decode_value(name)
            course_type = site.decode_value(course_type)
            course_info = site.decode_value(course_info)
            course_teacher = site.decode_value(course_teacher)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category, course_type, course_info, course_teacher)
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            self.category_id = int(request['request_params']['id'])
            category = site.find_category_by_id(int(self.category_id))

            return '200 OK', render('create_course.html', name=category.name, id=category.id)


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
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


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
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


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/teacher-list/')
class TeacherListView(ListView):
    queryset = site.teachers
    template_name = 'teacher_list.html'


@AppRoute(routes=routes, url='/create-teacher/')
class TeacherCreateView(CreateView):
    template_name = 'create_teacher.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('teacher', name)
        site.teachers.append(new_obj)


@AppRoute(routes=routes, url='/add-teacher/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_teacher.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['teachers'] = site.teachers
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        teacher_name = data['teacher_name']
        teacher_name = site.decode_value(teacher_name)
        teacher = site.get_teacher(teacher_name)
        course.add_teacher(teacher)  # - добавить функцию


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
