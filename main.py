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
import controllers.userLogController as userController
import controllers.imageController as imageController


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'aklsdfnkanxcjkzbxfjkhadfsks',
}


# set up paths
mappings = [
    ('/', indexController.index),
    ('/gallery', galleryController.index),
    ('/profile', profileController.index),
    ('/user', userController.index),
    ('/userFunctions', userController.userFunctions),
    ('/uploadImage', imageController.uploadImageHandler),
    ('/addLike', imageController.addLikeHandler),
    ('/getLikes', imageController.getLikeHandler),
    ('/comment', imageController.addCommentHandler),
    ('/deleteComment', imageController.deleteCommentHandler),
    ('/getCommentsTest', imageController.getCommentsHandler),
    ('/unlike', imageController.deleteLikeHandler)
    ('/gallery2', galleryController.gallery2)
#    ('/userLog', userController.loginPage.show)
]


app = webapp2.WSGIApplication(mappings, config=config, debug=True)




