from google.appengine.ext.webapp import template
import os





def render_template(handler,template_name, parameters):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, parameters)
    handler.response.out.write(html)