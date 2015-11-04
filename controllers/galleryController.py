
from google.appengine.ext import blobstore
import main
import app_global
import main
import models.imagesModel as imagesModel
import models.userModel as userModel
from google.appengine.ext import ndb
import json

# I use price ranges for my filtering. ie. 25-50. 
# So if you change the prices list after there are images in the datastore,
# you may get imprecise filtering. 

brands = ['Forever 21', 'Gap', 'PS', 'Other']
types = ['Shirt', 'Jeans', 'Shoes', 'Entire Body', 'Other']
prices = [25, 50, 100, 500, 1000]

# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
class index(main.index):
    
    #respond to HTTP GET requests
    def get(self):
        # images = imagesModels.getImages()
        
         

        #The following 10 lines of code just wipe the entire images, likes, comments datastore.
#        
#        users = userModel.Users.query()
#        for u in users.fetch():
#            u.key.delete()
#        
#        ims = imagesModel.Image.query()
#        for im in ims.fetch():
#            im.key.delete()
#
#        likes = imagesModel.Like.query()
#        for like in likes.fetch():
#                like.key.delete()
#                
#        coms = imagesModel.ImageComment.query()
#        for com in coms.fetch():
#                com.key.delete()
                
                
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
        if maxPrice == "":
            maxPrice = None
        
        #These things generate a price menu based on the prices. 
        #prices = [0, 25, 50] ==> priceOptions = ['$0-$25', '$25-$50', 'Over $50']
        priceOptions = list()
        lastValue = 0
        nextValue = prices[0]
        index = 0
        
        for i in range(0, len(prices)+1):
            if (i != len(prices)):
                priceOptions.append('$' + str(lastValue) + '-$' + str(nextValue))
            else:
                priceOptions.append('Over $' + str(nextValue))
            if (i < len(prices)-1):
                lastValue = nextValue
                index += 1
                nextValue = prices[index]
        
        
        #[25, 50]
        #['0-25', '25-50', 'Over 50'] 
        #This part just changes the option '25-50', etc. to an actual number for the filter.
        # '$0-$25' ==> minimumPrice = 0, maximumPrice = 25
        # Note: for maximum value. ie. over 1000, I use minimumPrice = highest + 1 (so 1001)
        # and maximumPrice = highest + 2 (so 1002).
        
        if maxPrice is not None:
            index = priceOptions.index(maxPrice)
            if index < len(priceOptions)-1:
                    maximumPrice = prices[index]
                    if (index-1 > -1):
                        minimumPrice = prices[index-1]
                    else:
                        minimumPrice = 0
            else:
                maximumPrice = prices[len(prices)-1] + 2
                minimumPrice = prices[len(prices)-1] + 1
        else:
            minimumPrice = None
            maximumPrice = None
       
        #This list is used to narrow the images down when filtering.
        restrictionList = list()
        restrictionList.append(minimumPrice)
        restrictionList.append(maximumPrice)
        restrictionList.append(brandName)
        restrictionList.append(clothingType)
        

        
        upload_url = blobstore.create_upload_url('/uploadImage')    
            
            
        params = {
#            'photos': images,
            #'photos_json': json.dumps(images),
            'user_id':self.session.get('user_id'),
            'user': self.session.get('user'),
            #'user_id': None, #testing when user is logged out
            'upload_url': upload_url,
            'brands': brands,
            'types': types,
            'prices': prices,
            'priceOptions': priceOptions
        }

 
        app_global.render_template(self,'gallery2.html', params)
    
    
class gallery2(main.index):
    def get(self):
        restrictionList = list()
        
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
            
        restrictionList.append(maximumPrice)
        restrictionList.append(brandName)
        restrictionList.append(clothingType)
        
        user_id = self.session.get('user_id')
        images = imagesModel.getImages(user_id, restrictionList)
        
        params = {
            user_id: user_id,
            images: images
        }
        app_global.render_template(self,'gallery2.html', params)    

                        
  
            
            
            
            
            