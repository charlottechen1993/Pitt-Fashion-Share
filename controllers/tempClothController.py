import webapp2
from webapp2_extras import sessions
import app_global
import indexController
import models.tempClothModel as tempClothModel

# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(indexController.index):
    
    def get(self):
        # images = imagesModels.getImages()
        
        
        params = {
            'user_id': self.session.get('user_id')      
        }
        
        app_global.render_template(self,'tempCloth.html', params)