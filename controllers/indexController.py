
import webapp2
from webapp2_extras import sessions

import app_global

# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(webapp2.RequestHandler):
    
    # start session    
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
 
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
 
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
    
    
    #respond to HTTP GET requests
    def get(self):
        # images = imagesModels.getImages()
        
        
        params = {'page_name':'Fashion Share', 
            'photo_name':'photo3', 
            'photo_name2':'photo2',
            'photo_name3':'photo',
            'cow1':'girl1.jpg', 
            'cow2':'girl2.jpg', 
            'cow3':'girl3.jpg', 
            'cow4':'girl4.jpg',
            'girl5':'girl9.jpg', 
            'girl6':'girl10.jpg', 
            'girl7':'girl11.jpg', 
            'girl8':'girl12.jpg',
            'user_id':self.request.get('user_id')
         }
        
        app_global.render_template(self,'index.html',{'page_name':'Fashion Share', 
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
                                                     })
		
