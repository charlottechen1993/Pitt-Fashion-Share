$(document).ready(function(){
//    $.ajax({
//        url: '/getPhotosJSON?user_id=' + 1,
//        data: {},
//        dataType: 'json',
////            contentType: "application/json",
//        success: function(data){
//            console.log(data);
//          //  data = JSON.parse(data);
//           //alert(JSON.stringify(data, null, 2));
//          //  alert(data);
//            for( var i = 0; i < data.length; i++ ) {
//                //$('#photos').append('<img src="' + data[i].image_url + '" alt="pretty kitty">');  
//                
//            }
//        },
//        error: function ( jqXHR, textStatus, errorThrown) {
//            alert(errorThrown);
//        }
//    });

});

 angularAPP.controller('imgCtrl', function($scope,$http){
     
    /*
        Purpose: Get images from server
        Functionality: dynamically load build html gallery for images,
                       and html for image modals
    */
    $.ajax({
        url: '/getPhotosJSON?user_id=' + 1,
        data: {},
        dataType: 'json',

        success: function(data){
            console.log(data);
          //  data = JSON.parse(data);
           //alert(JSON.stringify(data, null, 2));
          //  alert(data);
            for( var i = 0; i < data.length; i++ ) {
                //$('#photos').append('<img src="' + data[i].image_url + '" alt="pretty kitty">');  
                
                var img = {'image_url': data[i].image_url};
                $scope.populateGallery(img);
            }
        },
        error: function ( jqXHR, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });

     /*
        populates image gallery with images
     */
     $scope.populateGallery = function(img){

        $scope.images = [];

        $scope.$apply(function(){
            $scope.images.push(img);
        });
     }

    /*
        populates image modals
    */
     $scope.populateImgModal = function(){

     }

});