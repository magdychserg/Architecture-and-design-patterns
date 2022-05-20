import datetime
import os
from wavy.templates import rendering
from workers import workers


def all_view(request):

    # Используем шаблонизатор
    return '200 OK', rendering('index.html', workers=workers)


def director_view(request):

    return '200 OK', rendering('worker.html', workers=workers[0])


def accountant_view(request):

    return '200 OK', rendering('worker.html', workers=workers[1])


def specialist_view(request):

    return '200 OK', rendering('worker.html', workers=workers[2])


def about_view(request):

    # Просто возвращаем текст
    return '200 OK', "About"

def contact_view(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        now = datetime.datetime.now()
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        if not os.path.exists('messages'):
            os.mkdir('messages')
        with open(f'messages/message_{now.strftime("%d%m%Y")}_{now.strftime("%H%M%S")}.txt', 'w',
                  encoding='utf-8') as file:
            file.write(f'Нам пришло сообщение от {now.strftime("%d.%m.%Y")} в {now.strftime("%H:%M:%S")}!\n'
                       f'Отправитель: {email}\n'
                       f'Тема: {title}\n'
                       f'Текст: {text}')
        return '200 OK', rendering('contacts.html')
    else:
        return '200 OK', rendering('contacts.html')
