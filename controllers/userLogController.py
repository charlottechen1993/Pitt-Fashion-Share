import webapp2


import models.userModel as userModel

import app_global
import main

    
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(webapp2.RequestHandler):
        
    #respond to HTTP GET requests
    def get(self):
        method  = self.request.get('method')
        template = ''
        
        if method == 'newUser':
            un = self.request.get('un')
            pw = self.request.get('pw')
            user_key = userModel.Users.createNewUser(un, pw, None, None, None)
            template = 'login.html'
        else:
            template = 'login.html'
            
        app_global.render_template(self, template, {'id': user_key})
    

        
		  
		
class userFunctions():
    def newUser(self):
        userModel.createNewUser(un, pw, None, None, None)
       