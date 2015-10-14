from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import datetime

class Image(ndb.Model):
    categoryID = ndb.IntegerProperty()
    total = ndb.IntegerProperty()
    title = ndb.StringProperty()
    image_url = ndb.StringProperty()
    user = ndb.StringProperty()
    time_created = ndb.DateTimeProperty(auto_now_add=True)
    

    
def addImage(categoryID, total, title, image_url, user):
    image = Image()
    image.total = total
    image.categoryID = categoryID
    image.title = title
    image.image_url = image_url
    image.user = user
    image.put()
    
    
    
def getImages():
    result = list()
    query = Image.query()
   # query = query.order(Image.time_created)
    images = query.fetch()
    
    for i in range(0,len(images)):
        im = {}
        im['categoryID'] = images[i].categoryID
        im['total'] = images[i].total
        im['title'] = images[i].title
        im['image_url'] = images[i].image_url
        im['user_id'] = images[i].user
        im['img_id'] = images[i].key.id()
        result.append(im)
    return result