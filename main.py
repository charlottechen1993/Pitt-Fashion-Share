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

# set up paths
mappings = [
    ('/', indexController.index),
    ('/gallery', galleryController.index),
    # ('/catagory', catagoryController.index),
    ('/profile', profileController.index)
]


app = webapp2.WSGIApplication(mappings, debug=True)




