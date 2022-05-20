class Application:

    def __init__(self, routes: dict, front_controllers: list):
        """
        :param routes: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.routes = routes
        self.front_controllers = front_controllers

    def __call__(self, env, start_response):
        # текущий url
        path = env['PATH_INFO']

        if path in self.routes:
            # получаем view по url
            view = self.routes[path]
            request = {}
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
