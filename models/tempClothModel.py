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

#An image can have multiple clothItems, associated by the imgID property. 
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
    
# Adds a new clothItem and also finds the associated image and adds to its total price. 
def addClothItem(imgID, clothingType, brand, price):
    newCloth = clothItem(imgID, clothingType, brand, price)
    correspondingImage = Image.query(Image.imgID == imgID)
    correspondingImage.totalPrice += price

# Returns images with total prices within the range
def getImagesByPriceRange(min, max):
    images = Image.query()
    imagesBelow = images.filter(Image.totalPrice <= max)
    imagesAboveBelow = imagesBelow.filter(Image.totalPrice >= min)
    return imagesAboveBelow.fetch()

# Returns all clothItem instances for a given image/imageID. 
# Since an image can have more than one clothItem associated with it,
# this query can return multiple results. 
def getClothItems(imgID):
    return clothItem.query(clothItem.imgID == imgID).fetch()

# Returns all images with the matching brand
def getImagesByBrand(brand):
    return Image.query().filter(Image.brand == brand).fetch()

# Returns all images with the matching clothing type
def getImagesByType(clothingType):
    return Image.query().filter(Image.clothingType == clothingType).fetch()
   
# Returns all Images in the datastore.
def getImages():
    return Image.query().fetch()

# Returns all Likes for a particular image
def getLikesForPic(imgID):
    return Like.query(Like.imgID == imgID).fetch()

def getNumLikesForPic(imgID):
    return Like.query(Like.imgID == imgID).count()

# Returns True if found, False if not
# Used to determine if user has liked already, so to influence like/unlike option
def likedByUser(imgID, userID):
    allLikes = Like.query()
    thisImageLikes = allLikes.filter(im['img_id'] == Like.imgID)
    likedByYou = thisImageLikes.filter(Like.userID == str(user_id))
    cnt = likedByYou.count()
    if (cnt > 0):
        return True
    return False

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
    
    
