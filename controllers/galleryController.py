import webapp2
from google.appengine.ext import blobstore
import indexController
import app_global
import main
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(indexController.index):
    #respond to HTTP GET requests
    def get(self):
        # images = imagesModels.getImages()
        photo_list = []
        for i in range(1,17):
            photo = {}
            photo['name'] = 'girl'+ str(i) + '.jpg';
            if i%2==0:
                photo['adored'] = True;
            else:
                photo['adored'] = False;
            photo_list.append(photo)
            
            
        upload_url = blobstore.create_upload_url('/uploadImage')    
            
        params = {
            'photos':photo_list,
            'user_id':self.session.get('user_id'),
            'upload_url': upload_url
        }
        
        app_global.render_template(self,'gallery.html', params)