from google.appengine.ext import ndb
import datetime
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import json
import main
import app_global
from sets import Set

class ImageTag(ndb.Model):
    imageKey = ndb.StringProperty()
    tag_name = ndb.StringProperty()
    
class ImageComment(ndb.Model):
    userID = ndb.StringProperty()
    imgID = ndb.StringProperty()
    text = ndb.TextProperty()
    upload_date = ndb.StringProperty(default='')
    uploadedBy = ndb.StringProperty()
    
class Image(ndb.Model):
    categoryID = ndb.IntegerProperty()
    total = ndb.IntegerProperty()
    title = ndb.StringProperty()
    image_url = ndb.StringProperty()
    user = ndb.StringProperty()
    time_created = ndb.DateTimeProperty(auto_now_add=True)
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
    like.userID = str(app_global.unicode(userID))
    like.uploadedBy = app_global.unicode(username)
    like.put()
    
def deletePic(imgID):
    allImages = Image.query().fetch()
    for pic in allImages:
        if pic.key.id() == int(imgID):
            pic.key.delete()
    
def deleteLike(user_id, photo_id):
    like = Like.query(Like.userID==str(app_global.unicode(user_id)), Like.imgID==str(photo_id)).fetch(1)
    like[0].key.delete()
    
def getLikes():
    query = Like.query()
    likes = query.fetch()
    return likes

def create_comment(userID, text, imgID, username, time_created):
    comment = ImageComment()
    comment.imgID = str(imgID)
    comment.userID = str(app_global.unicode(userID))
    comment.text = text
    comment.uploadedBy = app_global.unicode(username)
    comment.upload_date = time_created
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

def addImage(categoryID, total, title, image_url, user, minPrice, maxPrice, priceRange, brand, clothingType, username, tag_name):
    image = Image()
    image.total = total
    image.categoryID = categoryID
    image.title = title
    image.image_url = image_url
    image.user = str(user)
    image.minPrice = minPrice
    image.maxPrice = maxPrice
    image.priceRange = priceRange
    image.brand = brand
    image.clothingType = clothingType
    image.uploadedBy = app_global.unicode(username)
    key = image.put()
    
#    users = ImageTag.query()
#    for u in users.fetch():
#        u.key.delete()
    
    for element in tag_name:
        image_tag = ImageTag()
        image_tag.imageKey = str(key.id())
        image_tag.tag_name = element
        image_tag.put()

    
    
def imagesYouLiked(userID):
    yourLikes = Like.query(Like.userID == userID)
    imgIDList = list()
    imgList = list()
    for like in yourLikes.fetch():
        imgIDList.append(like.imgID)
    for img in Image.query().fetch():
        if (img.key.id() in imgIDList):
            imgList.append(img)
    return imgList
    
#def get_image(image_id):
#    return ndb.Key(urlsafe=image_id).get()


def testGetImages(self):
    images = Image.query().fetch()
    app_global.render_template(self,'test.html', {'images':images})
    
class getPhotosJSONHandler(main.index):
    
    def get(self):
        result = list()

        #user_id = request.args.get(user_id)
        user_id = app_global.unicode(self.session.get('user_id'))
        profile = self.request.get('page')
        adored = self.request.get('adored')

        if user_id is None:
            user_id = -1

        #Not profile page
        if (profile != "profile"):
            queryImg = Image.query()            # get all images
        #Profile page
        else:
            #queryImg = Image.query()
            queryImg = Image.query(Image.user == str(user_id))
        
        queryImg = queryImg.order(-Image.time_created)
        queryLike = Like.query()            # get likes
        queryComment = ImageComment.query() # get comments
        
        
        #likedByYou = queryLike.filter(Like.userID == str(user_id)).fetch(projection=[Like.imgID])
        likes = queryLike.filter(Like.userID == str(user_id)).fetch(projection=[Like.imgID])
        
        likedByYou = set()
        # add imgID's of images the current user liked to the set likedByYou
        for item in likes:
            likedByYou.add(item.imgID)
     
        images = queryImg.fetch()
        
        if adored is not None and adored == "true":
            likes = Like.query(Like.userID == str(user_id))
            relevantPicIDs = []
            for instance in likes.fetch():
                relevantPicIDs.append(int(instance.imgID))
            queryImg = Image.query().order(-Image.time_created)
            allPics = queryImg.fetch()
            images = []
            for pic in allPics:
                if pic.key.id() in relevantPicIDs:
                    images.append(pic)
            queryLike = Like.query()
       
        
        for i in range(0,len(images)):
            im = {}
            key = str(images[i].key.id())
           
            tagObj = ImageTag.query(ImageTag.imageKey == key).fetch(projection=[ImageTag.tag_name])
            tag_arr = []
            for tag in tagObj:
                tag_arr.append(tag.tag_name)
            
            im['uploaded_by'] = images[i].uploadedBy
            im['tags'] = tag_arr
            im['img_id'] = str(images[i].key.id())
            # im['total'] = images[i].total
            im['title'] = images[i].title
            im['image_url'] = images[i].image_url
            im['user_id'] = images[i].user
            im['total_likes'] = queryLike.filter(Like.imgID == im['img_id']).count()

            comments = queryComment.filter(ImageComment.imgID ==  im['img_id'])
            comments = comments.order(-ImageComment.upload_date).fetch()              
            im['comments'] = [c.to_dict() for c in comments]
    
            if adored is not None and adored == "true" and (str(user_id) == str(images[i].user)):
                im['deleteOption'] = "active"
                im['profilePicOption'] = "active"

            if im['img_id'] in likedByYou:
                im['adored'] = True
            else:
                im['adored'] = False

                
            for elem in comments:
                elem.commentID = elem.key.id()
                if elem.userID == str(user_id):
                    elem.yours = 1 #i only check if it exists later on

            result.append(im)
            
        #return json.dumps(result[0])
        self.response.out.write(json.dumps(result))




class getImagesHandler(main.index):

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
            im['total_likes'] = queryLike.filter(Like.imgID == im['img_id']).count()

            comments = ImageComment.query(im['img_id'] == ImageComment.imgID)
            comments = comments.order(-ImageComment.time_created)
            im['comments'] = comments.fetch()

            if im['img_id'] in likedByYou:
                im['adored'] = True
            else:
                im['adored'] = False

            for elem in comments:
                elem.commentID = elem.key.id()
                if elem.userID == str(user_id):
                    elem.yours = 1 #i only check if it exists later on

            result.append(im)
            
        #return json.dumps(result[0])
        self.response.out.write(json.dumps(result))



def getImagesOld(user_id, restrictionsList):
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
    
