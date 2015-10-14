import webapp2
from google.appengine.ext import blobstore
import indexController
import app_global
import main
import models.imagesModel as imagesModel
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(indexController.index):
    #respond to HTTP GET requests
    def get(self):
        # images = imagesModels.getImages()
        
        photo_list = []
        
#        for i in range(1,17):
#            photo = {}
#            photo['name'] = 'girl'+ str(i) + '.jpg';
#            if i%2==0:
#                photo['adored'] = True;
#            else:
#                photo['adored'] = False;
#            photo_list.append(photo)
#            
        images = imagesModel.getImages()
        i = 0
        for img in images:
            i+=1
            if i%2==0:
                img['adored'] = True
            else:
                img['adored'] = False
            photo_list.append(img)
    
        upload_url = blobstore.create_upload_url('/uploadImage')    
            
        params = {
            'photos':photo_list,
            'user_id':self.session.get('user_id'),
            'upload_url': upload_url
        }
        
        app_global.render_template(self,'gallery.html', params)