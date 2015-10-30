import webapp2
import models.userModel as userModel
import app_global
from webapp2_extras import sessions
import indexController
# import path to models
import sys
sys.path.insert(0, '/models')

import app_global
import main

    
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(indexController.index):
        
    #respond to HTTP GET requests
    def get(self):
        user = self.session.get('user')
        
        params = {
            'user': user,
            'user_id': self.session.get('user_id')
        }
        
        app_global.render_template(self, 'profile.html', params)
		  
		
