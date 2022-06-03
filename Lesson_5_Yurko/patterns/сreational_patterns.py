import copy
import quopri


class User:

    def clone(self):
        return copy.deepcopy(self)


class Teacher(User):
    auto_id = 0

    def __init__(self, firstname, lastname):
        self.id = Teacher.auto_id
        Teacher.auto_id += 1
        self.firstname = firstname
        self.lastname = lastname
        self.teachers = []


class Student(User):
    auto_id = 0

    def __init__(self, firstname, lastname):
        self.id = Student.auto_id
        Student.auto_id += 1
        self.firstname = firstname
        self.lastname = lastname
        self.student = []


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, firstname, lastname):
        return cls.types[type_](firstname, lastname)


class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category, teacher):
        self.name = name
        self.category = category
        self.teacher = teacher
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category, teacher):
        return cls.types[type_](name, category, teacher)


class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, firstname, lastname):
        return UserFactory.create(type_, firstname, lastname)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category, teacher):
        return CourseFactory.create(type_, name, category, teacher)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
