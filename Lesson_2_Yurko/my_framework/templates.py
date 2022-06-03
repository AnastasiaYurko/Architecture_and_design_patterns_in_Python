from jinja2 import Template
import os


def template_build(template_name, folder='templates', **kwargs):
    file_path = os.path.join(folder, template_name)

    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())

    return template.render(**kwargs)
