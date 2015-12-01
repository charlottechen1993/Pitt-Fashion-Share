from google.appengine.ext import ndb
import datetime
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import json
import app_global
from imagesModel import Image


#An image can have multiple clothItems, associated by the imgID property. 
class clothItem(ndb.Model):
    imgID = ndb.StringProperty()
    clothingType = ndb.StringProperty()
    brand = ndb.StringProperty()
    price = ndb.IntegerProperty()
    x1 = ndb.IntegerProperty()
    y1 = ndb.IntegerProperty()
    x2 = ndb.IntegerProperty()
    y2 = ndb.IntegerProperty()
    width = ndb.IntegerProperty()
    height = ndb.IntegerProperty()


    
# Adds a new clothItem and also finds the associated image and adds to its total price. 
def addClothItem(imgID, clothingType, brand, price, x1, y1, x2, y2, width, height):

    newClothItem = clothItem()
    newClothItem.imgID = str(imgID)
    newClothItem.clothingType = clothingType
    newClothItem.brand = brand
    newClothItem.price = int(price)
    newClothItem.x1 = int(x1)
    newClothItem.y1 = int(y1)
    newClothItem.x2 = int(x2)
    newClothItem.y2 = int(y2)
    newClothItem.width = int(width)
    newClothItem.height = int(height)
    newClothItem.put()


  
    # correspondingImage = Image.query(Image.imgID == imgID)
    # correspondingImage.totalPrice += price

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
   

    
    
