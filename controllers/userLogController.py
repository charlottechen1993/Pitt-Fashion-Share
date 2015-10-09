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
        message = ''
        userList = list()
        
        if method == 'newUser':
            un = self.request.get('un')
            pw = self.request.get('pw')
            app_global.render_template(self, 'test.html', {'message':un, 'users':userList})
            # check that username does not already exist
#            user = userModel.Users.getUser(un)
#            if user:
#                message = 'Username already exist!'
#                template = 'index.html'
#            else:
#            user_key = userModel.createNewUser(un, pw)
#            template = 'profile.html'
#        elif method == 'login':
#            un = self.request.get('un')
#            pw = self.request.get('pw')
##            user = userModel.getUser(un, pw)
##            
##            if user > 0:
##                template = 'profile.html'
##                message = 'Logged in as ' + user[0].un
##            else:
##                template = 'index.html'
##                message = 'Login Fail!'
#            userList = userModel.getUsers()
#            template = 'test.html'
        else:
            template = 'login.html'
            app_global.render_template(self, template, {'message':message, 'users':userList})
    
        
		  
		
class userFunctions(webapp2.RequestHandler):
    
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
                user = userModel.Users.getUser(un)

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
                else:
                    template = 'index.html'
                    message = 'Login Fail!'
                userList = userModel.getUsers()
                template = 'test.html'
            else:
                template = 'login.html'
        
        app_global.render_template(self, template, {'message':message, 'users':userList})
    
        


       