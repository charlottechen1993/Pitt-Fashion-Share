import webapp2
import models.userModel as userModel
from google.appengine.api import mail
import app_global
from webapp2_extras import sessions
import indexController
    
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
# class index(webapp2.RequestHandler)
class index(indexController.index):
        
    #respond to HTTP GET requests
    def get(self):                                                  # /userFunctions
        user = self.session.get('user')
        message = self.request.get('message')
        
        params = {
            'user': user,
            'user_id': self.session.get('user_id'),
            'message': message
        }
        
        app_global.render_template(self, 'login.html', params)
    
        
		  
		
#class userFunctions(webapp2.RequestHandler):
class userFunctions(indexController.index):
    
    def post(self):
        method = self.request.get('method')
        un = self.request.get('un').strip()
        pw = self.request.get('pw').strip()
  
        
        if method!='logout' and (un == '' or pw ==''):
            message = 'You must fill out both email and password!'
            template = 'login.html'
            self.redirect('/user?message='+message)
            
        else:
            if method == 'newUser':                                 # /userFunctions?method=newUser
                #check that username does not already exist
                user = userModel.getUser(un, pw)

                if len(user) > 0:
                    message = 'ERROR: Username already exist!'
                    self.redirect('/user?message='+message)
                else:
                    user_key = userModel.createNewUser(un, pw)
                    template = 'profile.html'
                    mail.send_mail('admin@pittfashionshare.appspotmail.com', un, 'Registration', 'Thanks for registering with Pitt Fashion Share! Your account is now active.')
                

                    
                    # log newly registered user in
                    self.redirect('/userFunctions?method=login&un=' + un + '&pw=' + pw)
                    
            elif method == 'login':                                  # /userFunctions?method=login
                user = userModel.getUser(un, pw)

                
                if len(user) > 0:    # user login success
                    template = 'profile.html'
                    message = 'Logged in as ' + user[0].un
                    
                    self.session['user'] = user[0].un
                    self.session['user_id'] = user[0].user_id 
                    
                    self.redirect('/profile')
                else:
                    template = 'index.html'
                    message = 'ERROR: Login Fail!'
                    self.redirect('/user?message='+message)
            elif method == 'logout':                                   # /userFunctions?method=logout
                self.session['user'] = None
                self.session['user_id'] = None
                self.redirect('/user')
                
#        params = {
#            'message': message,
#            'user_id': self.session.get('user_id')
#        }        
#        
#
#        app_global.render_template(self, template, params)