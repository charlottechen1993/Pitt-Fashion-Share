import webapp2
import app_global
import main

class index(main.index):
    def get(self):
        params = {

         }
        app_global.render_template(self,'about.html', params)