import cgi
import urllib
import webapp2
from webapp2_extras import security
from google.appengine.ext import ndb


class Users(ndb.Model):
    un = ndb.StringProperty()
    pw = ndb.StringProperty()
    email = ndb.StringProperty()
    gender = ndb.StringProperty()       # m or f
    description = ndb.StringProperty()
    
    @property
    def pid(self):
        return self.key.id()


    
def createNewUser(un, pw):
    newUser = Users()
    secure_pw = security.generate_password_hash(pw, 'sha1')
    newUser.un = un
    newUser.pw = secure_pw
    newUser.put()
    
def getUser(un, pw):
    result = list()
  #  secure_pw = security.generate_password_hash(pw, 'sha1')
    query = Users.query(Users.un==un)
    user = query.fetch(1)
    
    if len(user) > 0:
        if security.check_password_hash(pw, user[0].pw):
            result.append(user[0])
    
    return result
    
    
def getUsers():
    userList = list()
    query = Users.query()
    
    for user in query:
        userList.append(user)
    
    return userList


def deleteUsers():
    ndb.delete_multi(
    Users.query().fetch(keys_only=True))