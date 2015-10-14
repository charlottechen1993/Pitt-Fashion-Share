import webapp2
import app_global
import models.imagesModel as imagesModel

# When webapp2 receives an HTTP GET request to the URL /, it instantiates the imageFunctions class
class imageFunctions(webapp2.RequestHandler):
    
    
    #respond to HTTP GET requests
    def get(self):
        method = self.request.get('method');
        categoryID = 0
        total = 59
        image_url = 'asdf'
        user = self.session.get('user_id')
        
        
        if method == 'upload':
            imagesModel.addImage(categoryID, total, title, image_url, user)