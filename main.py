#################################################################
#                  set up routing for website                   #
#################################################################


import webapp2
from google.appengine.ext.webapp import template
import sys
import os.path

import controllers.indexController as indexController
import controllers.galleryController as galleryController
import controllers.profileController as profileController
<<<<<<< HEAD
=======
import controllers.testGalleryController as testGalleryController
>>>>>>> f4490f0644c17459d5dbb68ef9e55ea4b6aac121

# set up paths
mappings = [
    ('/', indexController.index),
    ('/gallery', galleryController.index),
<<<<<<< HEAD
    # ('/catagory', catagoryController.index),
    ('/profile', profileController.index)
=======
    ('/profile', profileController.index),
    ('/testGallery', testGalleryController.index)
>>>>>>> f4490f0644c17459d5dbb68ef9e55ea4b6aac121
]


app = webapp2.WSGIApplication(mappings, debug=True)




