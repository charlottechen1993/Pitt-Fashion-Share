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