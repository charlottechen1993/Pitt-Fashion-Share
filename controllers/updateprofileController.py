
import sys
import webapp2
import models.userModel as userModel
from google.appengine.api import mail
import app_global
from webapp2_extras import sessions
import main
import time

    
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class

class update(main.index):
	def post(self):
		email = app_global.unicode(self.session.get('email'))
		item = self.request.get('item')
		print item

		if item == "name":
			newN = self.request.get('newName')
			print newN
			if len(newN) > 0:
				print "change name"
				userModel.changeName(email, newN)
				self.session['user'] = newN
			self.redirect("/updateprofile")


		elif item == "password":
			p1 = self.request.get('newPass1')
			p2 = self.request.get('newPass2')
			if p1 == p2:
				userModel.changePass(email, p1)
				self.session['pass'] = p1
			self.redirect("/updateprofile")


		elif item == "gender":
			gen = self.request.get('gender')
			userModel.changeGender(email, gen)
			self.session['gender'] = gen
			self.redirect("/updateprofile")


		else:
			des = self.request.get('des')
			userModel.changeGender(email, des)
			self.session['description'] = des
			self.redirect("/updateprofile")


class index(main.index):
    #respond to HTTP GET requests
    def get(self):
        
        user_id = app_global.unicode(self.session.get('user_id'))
        user = app_global.unicode(self.session.get('user'))
        description = app_global.unicode(self.session.get('description'))
        gender = app_global.unicode(self.session.get('gender'))
        email = app_global.unicode(self.session.get('email'))

        params = {
            'user_id': user_id,
            'user': user,
            'description': description,
            'gender': gender,
            'email': email
        }

 
        app_global.render_template(self,'updateprofile.html', params)