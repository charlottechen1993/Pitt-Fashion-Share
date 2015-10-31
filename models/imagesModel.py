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

class Image(ndb.Model):
    categoryID = ndb.IntegerProperty()
    total = ndb.IntegerProperty()
    title = ndb.StringProperty()
    image_url = ndb.StringProperty()
    user = ndb.StringProperty()
    time_created = ndb.DateTimeProperty(auto_now_add=True)
    comments = list()
    liked = ndb.IntegerProperty() #if initialized, yes
    minPrice = ndb.IntegerProperty()
    maxPrice = ndb.IntegerProperty()
    priceRange = ndb.StringProperty()
    brand = ndb.StringProperty()
    clothingType = ndb.StringProperty() # type as in shirt, jeans, etc. 
    uploadedBy = ndb.StringProperty()
    
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
    
def getLikes():
    query = Like.query()
    likes = query.fetch()
    return likes

def create_comment(userID, text, imgID, username):
    comment = ImageComment()
    comment.imgID = str(imgID)
    comment.userID = str(userID)
    comment.text = text
    comment.uploadedBy = username
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

def addImage(categoryID, total, title, image_url, user, minPrice, maxPrice, priceRange, brand, clothingType, username):
    image = Image()
    image.total = total
    image.categoryID = categoryID
    image.title = title
    image.image_url = image_url
    image.user = user
    image.minPrice = minPrice
    image.maxPrice = maxPrice
    image.priceRange = priceRange
    image.brand = brand
    image.clothingType = clothingType
    image.uploadedBy = username
    image.put()
    
#def get_image(image_id):
#    return ndb.Key(urlsafe=image_id).get()


def testGetImages(self):
    images = Image.query().fetch()
    app_global.render_template(self,'test.html', {'images':images})
    
class getPhotosJSONHandler(indexController.index):
    
    def get(self):
        result = list()

        #user_id = request.args.get(user_id)
        user_id = self.session.get('user_id')

        if user_id is None:
            user_id = -1

        queryImg = Image.query()     # get images
        queryLike = Like.query()     # get likes


      #  likes = queryLike.fetch()

        # get list of imgID's liked by you
        likedByYou = list()
        likedByYou = queryLike.filter(Like.userID == str(user_id)).fetch(projection=[Like.imgID])
    #    for i in range(0, len(likes)):
    #        likedByYou.append(likes[i].imgID)
    #        
        images = queryImg.fetch()
        for i in range(0,len(images)):
            im = {}
            im['categoryID'] = images[i].categoryID
            im['img_id'] = str(images[i].key.id())
            # im['total'] = images[i].total
            im['title'] = images[i].title
            im['image_url'] = images[i].image_url
            im['user_id'] = images[i].user
    #        im['total_likes'] = queryLike.filter(Like.imgID == im['img_id']).count()

            comments = ImageComment.query(im['img_id'] == ImageComment.imgID)
            comments = comments.order(-ImageComment.time_created)
            #im['comments'] = comments.fetch()

            if im['img_id'] in likedByYou:
                im['adored'] = True
            else:
                im['adored'] = False

            for elem in comments:
                elem.commentID = elem.key.id()
                if elem.userID == str(user_id):
                    elem.yours = 1 #i only check if it exists later on

            result.append(im)
            
        print(json.dumps(result[0]))
        #return json.dumps(result[0])
        self.response.out.write(json.dumps(result))


def getImages(user_id, restrictionsList):
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
        
    minPrice = restrictionsList[0]
    maxPrice = restrictionsList[1]
    brandName = restrictionsList[2]
    clothingType = restrictionsList[3]
    
    for i in range(0,len(images)):
        
        if (maxPrice is not None and minPrice is not None) and (images[i].minPrice >= maxPrice or images[i].maxPrice <= minPrice):
            continue
        
        if brandName is not None and images[i].brand != brandName:
            continue
        
        if clothingType is not None and images[i].clothingType != clothingType:
            continue
        
        im = {}
        im['categoryID'] = images[i].categoryID
        im['img_id'] = str(images[i].key.id())
        # im['total'] = images[i].total
        im['total'] = Like.query(im['img_id']==Like.imgID).count()
        im['title'] = images[i].title
        im['image_url'] = images[i].image_url
        im['user_id'] = images[i].user
        im['brand'] = images[i].brand
        im['clothingType'] = images[i].clothingType
        im['minPrice'] = images[i].minPrice
        im['maxPrice'] = images[i].maxPrice
        im['uploadedBy'] = images[i].uploadedBy
        im['priceRange'] = images[i].priceRange
        
        comments = ImageComment.query(im['img_id'] == ImageComment.imgID)
        comments = comments.order(-ImageComment.time_created)
        comments = comments.fetch()
        
        allLikes = Like.query()
        thisImageLikes = allLikes.filter(im['img_id'] == Like.imgID)
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
    




































































