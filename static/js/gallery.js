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
     
     $scope.images = [];
     $scope.comments = [];
     
     
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
            
            var photosLength;   // amount of photos to load
            
            // if current page contains '#homeCarousel' then the current page must be the index
            if( $('#homeCarousel').length > 0 && data.length>=12){
                photosLength = 12;
            }else{
                photosLength = data.length;
            }
                        
           // alert(JSON.stringify(data, null, 2));
            
            for( var i = 0; i < photosLength; i++ ) {
   
                var img = {
                    'image_url': data[i].image_url,
                    'img_id': data[i].img_id,
                    'title': data[i].title,
                    'adored': data[i].adored,
                    'comments': data[i].comments
                };
                
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

        $scope.$apply(function(){
            $scope.images.push(img);
        });
     }
     
     
     /*
        populates image comments
     */
     $scope.populateComments = function(comment){
         $scope.$apply(function(){
            $scope.comments.push(comment);
         });
     }

     
    /*
        add comment image modals
    */
     $scope.addComment = function($event, img_id, comment){

         $.ajax({
             url: '/comment?image_id='+img_id + '&comment='+comment,
             method: 'POST',
             success: function(data){
                console.log('comment added');
                // clear comment input 
                var input = document.getElementById("comment");
                input.setAttribute("value", "");
             }
         });
     }
     
     
     /*
        like image
     */
     $scope.handleLike = function($event, img_id){
         
         var item =  $(angular.element($event.currentTarget));
         var url;
         
         
         if(item.hasClass('heart-unfilled'))    // like image
         {
            url = '/addLike?photo_id=' + img_id;
            $(angular.element(item)).removeClass('heart-unfilled'); 
            $(angular.element(item)).addClass('heart-filled'); 
         }else{                                 // unlike image
            url = '/unLike?photo_id=' + img_id;
            $(angular.element(item)).removeClass('heart-filled'); 
            $(angular.element(item)).addClass('heart-unfilled'); 
         
         }
         
         
        $.ajax({
            url: url,
            success: function(data){
    
            }
        });
     }
     
     
     /*
        like image
     */
     $scope.unlikeImg = function($event, img_id){

        $.ajax({
            url: '/unlike?photo_id=' + img_id,
            success: function(data){
                // uncolor heart
                var item = $event.currentTarget;
                $(angular.element(item)).removeClass('heart-filled'); 
                $(angular.element(item)).addClass('heart-unfilled'); 
            }
        });
     }

});