from google.appengine.ext import ndb
import datetime
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import json
import controllers.indexController as indexController
import app_global

class ImageComment(ndb.Model):
    userID = ndb.StringProperty()
    imgID = ndb.StringProperty()
    text = ndb.TextProperty()
    time_created = ndb.DateTimeProperty(auto_now_add=True) 
    uploadedBy = ndb.StringProperty()
    yours = ndb.IntegerProperty() #I  just set it something if true since bool didnt work
                                  # so (if yours) then it shows on the html

        
#An image can have multiple clothItems. 
class clothItem(ndb.Model):
    imgID = ndb.StringProperty()
    clothingType = ndb.StringProperty()
    brand = ndb.StringProperty()
    price = ndb.IntegerProperty()
    
class Image(ndb.Model):
    totalPrice = ndb.IntegerProperty()
    title = ndb.StringProperty()
    image_url = ndb.StringProperty()
    user = ndb.StringProperty()
    time_created = ndb.DateTimeProperty(auto_now_add=True)
    comments = list()
    liked = ndb.IntegerProperty() #if initialized, yes
    uploadedBy = ndb.StringProperty()

def getImagesByPriceRange(min, max):
    images = Image.query()
    imagesBelow = images.filter(Image.totalPrice <= max)
    imagesAboveBelow = imagesBelow.filter(Image.totalPrice >= min)
    return imagesAboveBelow.fetch()

def getImages():
    return Image.query()

def getLikesForPic(imgID):
    return Like.query(Like.imgID == imgID)

def getNumLikesForPic(imgID):
    return Like.query(Like.imgID == imgID).count()

#returns 1 if found, None if not
def likedByUser(imgID, userID):
    allLikes = Like.query()
    thisImageLikes = allLikes.filter(im['img_id'] == Like.imgID)
    likedByYou = thisImageLikes.filter(Like.userID == str(user_id))
    cnt = likedByYou.count()
    if (cnt > 0):
        return 1
    return None

class Like(ndb.Model):
    imgID = ndb.StringProperty()
    userID = ndb.StringProperty()
    uploadedBy = ndb.StringProperty()

def addLike(userID, imgID, username):
    like = Like()
    like.imgID = str(imgID)
    like.userID = str(userID)
    like.uploadedBy = username
    like.put()
    
    
