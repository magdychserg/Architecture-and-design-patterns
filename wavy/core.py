class Application:

    def __init__(self, routes: dict, front_controllers: list):
        """
        :param routes: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.routes = routes
        self.front_controllers = front_controllers

    def parse_input_data(self, data: str):
        # Парсим строку (разбиваем по &)
        result_dict = {}
        if data:
            params = data.split('&')
            for i in params:
                n, m = i.split('=')
                result_dict[n] = m
        return result_dict

    def parse_wsgi_input_data(self, data: bytes):
        # Декодируем байты и передаем в parse_input_data
        result_dict = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result_dict = self.parse_input_data(data_str)
        return result_dict

    def get_wsgi_input_data(self, env):
        # Определяет объем контента и читает его
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __call__(self, env, start_response):
        # текущий url
        path = env['PATH_INFO']

        if path[-1] != '/':
            path = f'{path}/'

        # Получаем все данные запроса
        method = env['REQUEST_METHOD']
        data = self.get_wsgi_input_data(env)
        data = self.parse_wsgi_input_data(data)

        query_string = env['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.routes:
            # получаем view по url
            view = self.routes[path]
            request = {'method': method, 'data': data, 'request_params': request_params}
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
            start_response('404 PAGE NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Page not found!"]
