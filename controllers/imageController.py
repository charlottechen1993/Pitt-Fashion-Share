import webapp2
import app_global
import models.imagesModel as imagesModel
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
import indexController

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
            
            
class uploadImageHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads()
        blob_info = upload_files[0]
        type = blob_info.content_type

        if type in ['image/jpeg', 'image/png']: 

            title = self.request.get('title')
            user = self.request.get('user_id')
            categoryID = 0
            total = 59
            image_url = images.get_serving_url(blob_info.key())
            imagesModel.addImage(categoryID, total, title, image_url, user)

            
            params = {
                'user_id':1
            }

            app_global.render_template(self,'index.html', params)
    
    
    
class addLikeHandler(indexController.index):
    
    def get(self):
        photo_id = self.request.get('photo_id')
        user_id = self.session.get('user_id')
        imagesModel.addLike(user_id, photo_id)    
    
        params = {
            'user_id':self.session.get('user_id'),
        }

        app_global.render_template(self,'index.html', params)
    
    
        
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
        

    
    
    
    
    
    