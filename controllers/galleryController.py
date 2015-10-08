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
            photo = {}
            photo['name'] = 'girl'+ str(i) + '.jpg';
            if i%2==0:
                photo['adored'] = True;
            else:
                photo['adored'] = False;
            photo_list.append(photo)
            
        app_global.render_template(self,'gallery.html', {'photos':photo_list})