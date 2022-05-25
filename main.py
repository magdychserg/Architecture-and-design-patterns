from framework.core import Application
from framework.templates import render_
from models import TrainingSite
from logging_mod import Logger, debug


site = TrainingSite()
logger = Logger('main')


def main_view(request):
    logger.log('Список курсов')
    return '200 OK', render_('course_list.html', objects_list=site.courses)


@debug
def create_course(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        name = data['name'].encode('utf-8').decode('utf-8')
        category_id = data.get('category_id')
        print(category_id)
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            site.courses.append(course)
        return '200 OK', render_('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render_('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        print('==>', data['name'].encode('utf-8').decode('utf-8'))
        name = data['name'].encode('utf-8').decode('utf-8')
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        return '200 OK', render_('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render_('create_category.html', categories=categories)


def secret_controller(request):
    request['secret'] = 'secret'


routes = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category
}


front_controllers = [
    secret_controller
]

app = Application(routes, front_controllers)


@app.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render_('course_list.html', objects_list=site.courses)


@app.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render_('category_list.html', objects_list=site.categories)
