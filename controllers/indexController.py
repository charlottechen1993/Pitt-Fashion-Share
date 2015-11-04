import webapp2
import app_global
import main

# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(main.index):
    
    #respond to HTTP GET requests
    def get(self):
        # images = imagesModels.getImages()
        
        
        params = {
            'logo':'pitt_logo.png',
            'photo_name':'photo3.jpg', 
            'photo_name2':'photo2.jpg',
            'photo_name3':'photo.jpg',
            'user': self.session.get('user'),
            'user_id':self.session.get('user_id')
         }
        
        app_global.render_template(self,'index.html', params)