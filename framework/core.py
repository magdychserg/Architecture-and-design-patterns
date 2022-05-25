class Application:

    def __init__(self, urlpatterns: dict, front_controllers: list):
        """
        :param urlpatterns: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def add_route(self, url):
        # паттерн декоратор
        def inner(view):
            self.urlpatterns[url] = view

        return inner

    def parse_input_data(self, data: str):
        # Берет строку, разделяет ее по & и кладет в словарь
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def parse_wsgi_input_data(self, data: bytes):
        # Берет байты, декодирует и передает в parse_input_data
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, env):
        # Определяет объем контента и читает его
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __call__(self, env, start_response):
        # текущий url
        path = env['PATH_INFO']

        # добавление закрывающего слеша
        if path[-1] != '/':
            path = f'{path}/'

        # Получаем все данные запроса
        method = env['REQUEST_METHOD']
        data = self.get_wsgi_input_data(env)
        data = self.parse_wsgi_input_data(data)

        query_string = env['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urlpatterns:
            # получаем view по url
            view = self.urlpatterns[path]
            request = {}
            # добавляем параметры запросов
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params
            # добавляем в запрос данные из front controllers
            for controller in self.front_controllers:
                controller(request)
            # вызываем view, получаем результат
            code, text = view(request)
            # возвращаем заголовки
            start_response(code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа
            return [text.encode('utf-8')]
        else:
            # Если url нет в urlpatterns - то страница не найдена
            # return '404 WHAT', [b'404 UNKNOWN COLOR!!!!!!1']
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'404 UNKNOWN COLOR!!!!!!1']