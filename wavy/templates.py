from jinja2 import Template
import os


def rendering(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон, для примера меняем путь на ../templates
    :param kwargs: параметры
    :return:
    """
    file_path = os.path.join(folder, template_name)
    # Открываем шаблон по имени
    with open(file_path, encoding='utf-8') as f:
        # Читаем
        template = Template(f.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)


if __name__ == '__main__':
    # Пример использования
    output_test = rendering('index.html', workers={
        'position': 'director',
        'first_name': 'Nikita',
        'last_name': 'Driven'
    })
    # print(output_test)