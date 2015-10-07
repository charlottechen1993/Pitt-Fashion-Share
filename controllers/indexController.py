
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
                                                      'photo_name':'male-photo.jpg', 
                                                      'photo_name2':'test.jpg',
                                                      'photo_name3':'sketch.jpg',
                                                      'cow1':'girl1.jpg', 
                                                      'cow2':'girl2.jpg', 
                                                      'cow3':'girl3.jpg', 
                                                      'cow4':'girl4.jpg',
                                                      'girl5':'girl9.jpg', 
                                                      'girl6':'girl10.jpg', 
                                                      'girl7':'girl11.jpg', 
                                                      'girl8':'girl12.jpg',
                                                     })
		
		
