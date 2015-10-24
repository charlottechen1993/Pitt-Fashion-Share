from google.appengine.ext import ndb
import datetime
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
#
#def get_user_email():
#  result = None
#  user = users.get_current_user()
#  if user:
#    result = user.email()
#  return result

class ImageComment(ndb.Model):
    userID = ndb.StringProperty()
    imgID = ndb.StringProperty()
    text = ndb.TextProperty()
    time_created = ndb.DateTimeProperty(auto_now_add=True) 
    yours = ndb.IntegerProperty() #I  just set it something if true since bool didnt work
                                  # so (if yours) then it shows on the html

class Image(ndb.Model):
    categoryID = ndb.IntegerProperty()
    total = ndb.IntegerProperty()
    title = ndb.StringProperty()
    image_url = ndb.StringProperty()
    user = ndb.StringProperty()
    time_created = ndb.DateTimeProperty(auto_now_add=True)
    comments = list()
    liked = ndb.IntegerProperty() #using same way as ImageComment.yours
    
class Like(ndb.Model):
    imgID = ndb.StringProperty()
    userID = ndb.StringProperty()

def addLike(userID, imgID):
    like = Like()
    like.imgID = str(imgID)
    like.userID = str(userID)
    like.put()
    
def getLikes():
    query = Like.query()
    likes = query.fetch()
    return likes

def create_comment(userID, text, imgID):
    comment = ImageComment()
    comment.imgID = str(imgID)
    comment.userID = str(userID)
    comment.text = text
    comment.put()
   
def get_comments(imgID):
    result = list()
    q = ImageComment.query(ImageComment.imgID == imgID)
    q = q.order(-ImageComment.time_created)
    comments = q.fetch()
#    for comment in q.fetch(1000):
#        result.append(comment)
    return comments

def get_all_comments():
    q = ImageComment.query()
    comments = q.fetch()
    return comments


    
def addImage(categoryID, total, title, image_url, user):
    image = Image()
    image.total = total
    image.categoryID = categoryID
    image.title = title
    image.image_url = image_url
    image.user = user
    image.put()
    
#def get_image(image_id):
#    return ndb.Key(urlsafe=image_id).get()
    
def getImages(user_id):
    result = list()
    queryImg = Image.query()
    #query = query.order(Image.time_created)
    images = queryImg.fetch()
    
    queryLike = Like.query(Like.userID==str(user_id))
    likes = queryLike.fetch()
    
    #dictLikes = dict((i['photoID'], i['userID']) for i in likes)
    dictLikes = list()
    for i in range(0, len(likes)):
        dictLikes.append(likes[i].imgID)
    
    for i in range(0,len(images)):
        im = {}
        im['categoryID'] = images[i].categoryID
        im['img_id'] = str(images[i].key.id())
        # im['total'] = images[i].total
        im['total'] = Like.query(im['img_id']==Like.imgID).count()
        im['title'] = images[i].title
        im['image_url'] = images[i].image_url
        im['user_id'] = images[i].user
       
        
        comments = ImageComment.query(im['img_id'] == ImageComment.imgID)
        comments = comments.order(-ImageComment.time_created)
        comments = comments.fetch()
        
        
        allLikes = Like.query()
        thisImageLikes = allLikes.filter(im['img_id'] == Like.imgID) #problem is here
        likedByYou = thisImageLikes.filter(Like.userID == str(user_id))
        cnt = likedByYou.count()
        
        
        #None value if not liked. 
        if cnt > 0:
            im['likedByYou'] = thisImageLikes.count()
            specificLike = likedByYou.fetch(1)[0]
            im['yourLikeID'] = specificLike.key.id()
        
        for elem in comments:
            elem.commentID = elem.key.id()
            if elem.userID == str(user_id):
                elem.yours = 1 #i only check if it exists later on
        
        im['comments'] = comments
        
        if im['img_id'] in dictLikes:
            im['adored'] = True
        else:
            im['adored'] = False
        
        result.append(im)
    return result