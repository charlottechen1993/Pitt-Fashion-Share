
import webapp2
from webapp2_extras import sessions
import indexController
import app_global

# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(indexController.index):
    
    
    #respond to HTTP GET requests
    def get(self):
        # images = imagesModels.getImages()
        
        user_id =  self.session.get('user_id')
        
        params = {
            'page_name':'Fashion Share', 
            'photo_name':'photo3.jpg', 
            'photo_name2':'photo2.jpg',
            'photo_name3':'photo.jpg',
            'cow1':'girl1.jpg', 
            'cow2':'girl2.jpg', 
            'cow3':'girl3.jpg', 
            'cow4':'girl4.jpg',
            'girl5':'girl9.jpg', 
            'girl6':'girl10.jpg', 
            'girl7':'girl11.jpg', 
            'girl8':'girl12.jpg',
            'user_id': user_id
        }
        
        app_global.render_template(self,'index.html', params)
		
