
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
        app_global.render_template(self,'index.html',{'page_name':'Thrifty Clothes', 
                                                      'photo_name':'test.jpg', 
                                                      'cow1':'Baby-Cow.jpg', 
                                                      'cow2':'Double-Cow.jpg', 
                                                      'cow3':'Fluffy-Cow.jpg', 
                                                      'cow4':'Orange-Cow.jpg'})
		
		
