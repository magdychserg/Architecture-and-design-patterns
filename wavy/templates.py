from jinja2 import Environment, FileSystemLoader


def rendering(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    tmpl = env.get_template(template_name)
    return tmpl.render(**kwargs)