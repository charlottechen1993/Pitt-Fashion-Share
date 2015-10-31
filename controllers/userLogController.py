import webapp2
import models.userModel as userModel
import app_global
from webapp2_extras import sessions
import indexController
    
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
# class index(webapp2.RequestHandler)
class index(indexController.index):
        
    #respond to HTTP GET requests
    def get(self):
        user = self.session.get('user')
        
        params = {
            'user': user,
            'user_id': self.session.get('user_id')
        }
        
        app_global.render_template(self, 'login.html', params)
    
        
		  
		
#class userFunctions(webapp2.RequestHandler):
class userFunctions(indexController.index):
    
    def post(self):
        method = self.request.get('method')
        un = self.request.get('un').strip()
        pw = self.request.get('pw').strip()
        userList = list()
        message = ''
        
        if un == '' or pw =='':
            message = 'You must fill out both username and password!'
        else:
            if method == 'newUser':
                #check that username does not already exist
                user = userModel.getUser(un, pw)

                if user:
                    message = 'Username already exist!'
                    template = 'login.html'
                else:
                    user_key = userModel.createNewUser(un, pw)
                    template = 'profile.html'
            elif method == 'login':
                user = userModel.getUser(un, pw)

                if len(user) > 0:    # user login success
                    template = 'profile.html'
                    message = 'Logged in as ' + user[0].un
                    
                    self.session['user'] = user[0].un
                    self.session['user_id'] = user[0].user_id 
                else:
                    template = 'index.html'
                    message = 'Login Fail!'
                userList = userModel.getUsers()
                template = 'test.html'
            else:
                template = 'login.html'
                
        params = {
            'message': message,
            'user_id': self.session.get('user_id')
        }        
        
        app_global.render_template(self, template, params)