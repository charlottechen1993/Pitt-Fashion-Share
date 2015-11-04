import cgi
import urllib
import webapp2
from webapp2_extras import security
from google.appengine.ext import ndb



class Users(ndb.Model):
    un = ndb.StringProperty()           # name, personal identifier
    pw = ndb.StringProperty()
    email = ndb.StringProperty()        # unique login credential
    gender = ndb.StringProperty()       # m or f
    description = ndb.StringProperty()
    
    @property
    def pid(self):
        return self.key.id()


    
def createNewUser(email, un, pw, gender):
    newUser = Users()
    secure_pw = security.generate_password_hash(pw, 'sha1')

    newUser.email = email
    newUser.un = un
    newUser.pw = secure_pw
    newUser.gender = gender
    newUser_key = newUser.put()
    return newUser_key

    
def getUser(email, pw):
    result = list()
    secure_pw = security.generate_password_hash(pw, 'sha1')
    query = Users.query(Users.email==email)
    user = query.fetch(1)
    
    
    if len(user) > 0:
        if security.check_password_hash(pw, user[0].pw):
            user[0].user_id = user[0].key.id()
            result.append(user[0])
    
    return result
    
    
def getUsers():
    userList = list()
    query = Users.query().fetch()
    

    for user in query:
        userList.append(user)
    
    return userList


def deleteUsers():
    ndb.delete_multi(
    Users.query().fetch(keys_only=True))