import webapp2

# import path to models
import sys
sys.path.insert(0, '/models')

import app_global
import main
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(webapp2.RequestHandler):
    #respond to HTTP GET requests
    def get(self):
        # images = imagesModels.getImages()
        photo_list = []
        for i in range(1,17):
            photo_list.append('girl'+ str(i) + '.jpg')
        app_global.render_template(self,'gallery.html',{'photos':photo_list})