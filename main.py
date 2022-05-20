
from wavy.core import Application
from wavy.routes import routes


def worker_controller(request):
    # пример Front Controller
    request['workers'] = {
        'position': 'director',
        'first_name': 'Nikita',
        'last_name': 'Driven'
    }


front_controllers = [
    worker_controller
]

app = Application(routes, front_controllers)

# Запуск:
# gunicorn main:app
