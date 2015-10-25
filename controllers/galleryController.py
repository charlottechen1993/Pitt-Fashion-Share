import webapp2
from google.appengine.ext import blobstore
import indexController
import app_global
import main
import models.imagesModel as imagesModel
import json



# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(indexController.index):
    #respond to HTTP GET requests
    def get(self):
        # images = imagesModels.getImages()
  
        
#        for i in range(1,17):
#            photo = {}
#            photo['name'] = 'girl'+ str(i) + '.jpg';
#            if i%2==0:
#                photo['adored'] = True;
#            else:
#                photo['adored'] = False;
#            photo_list.append(photo)

        #getImages(user_id, maxPrice, brandName, clothingType)
#       None is used to not consider that restriction

        user_id = self.session.get('user_id')
    
        maxPrice = self.request.get('maxPrice')
        brandName = self.request.get('brand')
        clothingType = self.request.get('clothingType')
        
        if brandName == "":
            brandName = None
        if clothingType == "":
            clothingType = None
        
        try:
            maximumPrice = int(maxPrice)
        except:
            maximumPrice = None
            
        restrictionList = list()
        restrictionList.append(maximumPrice)
        restrictionList.append(brandName)
        restrictionList.append(clothingType)
    
        images = imagesModel.getImages(user_id, restrictionList)
        
        brands = ['Asian', 'Forever 21', 'Gap', 'PS', 'Other']
        types = ['Shirt', 'Jeans', 'Shoes', 'Entire Body', 'Other']
        prices = [25, 50, 100, 500, 1000]
    
        upload_url = blobstore.create_upload_url('/uploadImage')    
            
        params = {
            'photos': images,
            #'photos_json': json.dumps(images),
            'user_id':self.session.get('user_id'),
            'upload_url': upload_url,
            'brands': brands,
            'types': types,
            'prices': prices
        }

 
        app_global.render_template(self,'gallery.html', params)
    
    
class gallery2(indexController.index):
    def get(self):
         app_global.render_template(self,'gallery2.html', {})    