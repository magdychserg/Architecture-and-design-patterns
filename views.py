from wavy.templates import rendering
from workers import workers


def all_view(request):
    # print(request)
    # Используем шаблонизатор
    return '200 OK', rendering('index.html', workers=workers)


def director_view(request):
    # print(request)
    return '200 OK', rendering('worker.html', workers=workers[0])


def accountant_view(request):
    # print(request)
    return '200 OK', rendering('worker.html', workers=workers[1])


def specialist_view(request):
    # print(request)
    return '200 OK', rendering('worker.html', workers=workers[2])


def about_view(request):
    # print(request)
    # Просто возвращаем текст
    return '200 OK', "About"