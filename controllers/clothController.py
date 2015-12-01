import webapp2
from webapp2_extras import sessions
import app_global
import main
import models.clothModel as clothModel

# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(main.index):
    
    def get(self):
    	imgID = self.request.get('imgID')
    	clothingType = self.request.get('clothingType')
    	brand = self.request.get('brand')
    	price = self.request.get('price')
    	descriptopn = self.request.get('description')
    	x1 = self.request.get('x1')
    	y1 = self.request.get('y1')
    	x2 = self.request.get('x2')
    	y2 = self.request.get('y2')
    	width = self.request.get('width')
    	height = self.request.get('height')

    	clothModel.addClothItem(imgID, clothingType, brand, price, x1, y1, x2, y2, width, height)
        
 