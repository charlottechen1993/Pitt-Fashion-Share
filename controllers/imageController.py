import webapp2
import app_global
import datetime
import logging
import models.imagesModel as imagesModel
import indexController
import galleryController
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

# When webapp2 receives an HTTP GET request to the URL /, it instantiates the imageFunctions class
#class imageFunctions(webapp2.RequestHandler):
#    
#    
#    #respond to HTTP GET requests
#    def get(self):
#        method = self.request.get('method');
#        categoryID = 0
#        total = 59
#        image_url = 'asdf'
#        user = self.session.get('user_id') # may need to save user_id into html page, hidden input
#        
#        
#        if method == 'upload':
#            imagesModel.addImage(categoryID, total, title, image_url, user)


class addCommentHandler(indexController.index):
    def post(self):
        imgID = self.request.get('image_id')
        userID = self.session.get('user_id')
        if userID: 
            text = self.request.get('comment')
            imagesModel.create_comment(userID, text, imgID)
            self.redirect('/gallery')
        else:
            self.redirect('/')
            
class deleteCommentHandler(indexController.index):
    def post(self):
        commentID = self.request.get('commentID')
        commentKey = ndb.Key(imagesModel.ImageComment, int(commentID))
        if commentKey is not None:
            commentKey.delete()
        self.redirect('/gallery')
            
class uploadImageHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads()
        blob_info = upload_files[0]
        type = blob_info.content_type

        if type in ['image/jpeg', 'image/png']: 
            title = self.request.get('title')
            user = self.request.get('user_id')
            priceRange = self.request.get('priceRange')
            brand = self.request.get('brand')
            clothingType = self.request.get('clothingType')
        
            prices = galleryController.prices
        
            #These things generate a dynamic price menu based on the prices. 
            #prices = [0, 25, 50] ==> priceOptions = ['$0-$25', '$25-$50', 'Over $50']
            priceOptions = list()
            lastValue = 0
            nextValue = prices[0]
            index = 0
        
            for i in range(0, len(prices)+1):
                if (i != len(prices)):
                    priceOptions.append('$' + str(lastValue) + '-$' + str(nextValue))
                else:
                    priceOptions.append('Over $' + str(nextValue))
                if (i < len(prices)-1):
                    lastValue = nextValue
                    index += 1
                    nextValue = prices[index]
        
             #[25, 50]
        #['0-25', '25-50', 'Over 50'] 
        #This part just changes the option '25-50', etc. to an actual number for the filter.
        # '$0-$25' ==> minimumPrice = 0, maximumPrice = 25
        # Note: for maximum value. ie. over 1000, I use minimumPrice = highest + 1 (so 1001)
        # and maximumPrice = highest + 2. 
            
            if priceRange is not None:
                index = priceOptions.index(priceRange)
                if index < len(priceOptions)-1:
                    picPriceMax = prices[index]
                    if (index-1 > -1):
                        picPriceMin = prices[index-1]
                    else:
                        picPriceMin = 0
                else:
                    picPriceMax = prices[len(prices)-1] + 2
                    picPriceMin = prices[len(prices)-1] + 1
            else:
                picPriceMin = None
                picPriceMax = None
         
            categoryID = 0
            total = 59
            image_url = images.get_serving_url(blob_info.key())
            imagesModel.addImage(categoryID, total, title, image_url, user, picPriceMin, picPriceMax, brand, clothingType)

            
            params = {
                'user_id':1
            }

            #self.redirect('/gallery')
            app_global.render_template(self,'index.html', params)
    
class deleteLikeHandler(indexController.index):
    def get(self):
        likeID = self.request.get('likeID')
        likeKey = ndb.Key(imagesModel.Like, int(likeID))
        if likeID is not None:
            likeKey.delete()
        self.redirect('gallery')
    
class addLikeHandler(indexController.index):
    def get(self):
        photo_id = self.request.get('photo_id')
        user_id = self.session.get('user_id')
        imagesModel.addLike(user_id, photo_id)    
        self.redirect('/gallery')
    
# test        
class getLikeHandler(indexController.index):
    
    def get(self):
        likes = imagesModel.getLikes()
        
                
        template = 'test.html'
      
                
        params = {
            'message': self.session.get('user_id'),
            'user_id': self.session.get('user_id'),
            'likes': likes
        }        
        
        app_global.render_template(self, template, params)
        

# test
class getCommentsHandler(indexController.index):
    
    def get(self):
        comments = imagesModel.get_all_comments()
        likes = imagesModel.getLikes()
        user_id = self.session.get('user_id')
        
        restrictions = list()
        restrictions.append(None)
        restrictions.append(None)
        restrictions.append(None)
        restrictions.append(None)
        
        images = imagesModel.getImages(user_id, restrictions)
        template = 'test.html'
        params = {
            'message': self.session.get('user_id'),
            'user_id': self.session.get('user_id'),
            'likes': likes,
            'comments': comments,
            'images': images
        }        
        
        app_global.render_template(self, template, params)
    
    
    
    
    
    