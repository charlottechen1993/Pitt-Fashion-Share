

 angularAPP.controller('imgCtrl', function($scope,$http){
     $scope.tags = [];
     $scope.images = [];
     $scope.comments = [];
     $scope.items = [];
     $scope.showAllPhotos = true;
     $scope.select_image_url = '';
     $scope.showAdoredOnly = false;
     $scope.showCategoryDrop = false;
     
     var page;
     if( $('#profilePage').length > 0)
     {
         page = 'profile';
     }
     
     
    /*
        Purpose: Get images from server
        Functionality: dynamically load build html gallery for images,
                       and html for image modals
    */
    $.ajax({
        url: '/getPhotosJSON?user_id=' + 1 + '&page=' + page + '&adored=' + $scope.showAdoredOnly,
        data: {},
        dataType: 'json',

        success: function(data){
            //console.log(data);
           // printJSON(data[0].tags);
            //printJSON(data[0].tags[0]);
            
            var page_url = window.location.href;
            var isProfilePage = false, isGalleryPage = false;
            
            if(page_url.indexOf("profile") > -1){
                isProfilePage = true;
            }else if(page_url.indexOf("gallery") > -1){
                isGalleryPage = true;
                $scope.showCategoryDrop = true;
            }
            
            var photosLength;   // amount of photos to load
            
            // if current page contains '#homeCarousel' then the current page must be the index
            if( $('#homeCarousel').length > 0 && data.length>=15){
                photosLength = 15;
            }else{
                photosLength = data.length;
            }
                        
           // alert(JSON.stringify(data, null, 2));
            
            for( var i = 0; i < photosLength; i++ ) {
                $scope.tags = [];
                var likes;
                
                if(data[i].total_likes == 0){
                    likes = '';
                }else{
                    likes = data[i].total_likes;
                }
                
                var img = {
                    'profilePage': isProfilePage,
                    'galleryPage': isGalleryPage,
                    'image_url': data[i].image_url,
                    'img_id': data[i].img_id,
                    'title': data[i].title,
                    'adored': data[i].adored,
                    'comments': data[i].comments,
                    'total_likes': likes,
                    'tags': data[i].tags,
                    'deleteOption': data[i].deleteOption,
                    'profilePicOption': data[i].profilePicOption,
                };
                
                //console.log(img['adored']);
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

        if(comment=='' || comment==undefined){
            return;
        }

         $.ajax({
             url: '/comment?image_id='+img_id + '&comment='+comment,
             method: 'POST',
             dataType: 'json',
             success: function(data){
                console.log('comment added');
                // clear comment input 
                var input = document.getElementById("commentInput");
                input.value = "";
                
                 
                // now append new comment to dom
                var cmtChild = '<div class="row cmt eq-row">' +
                                    '<div class="col-sm-3 left-inner-cmt eq-col">' +
                                        '<p class="center">' + data.user + ' says</p>' + 
                                   '</div>' +
                                   '<div class="col-sm-9 right-inner-cmt eq-col">' +
                                        '<p class="center">' + comment + '</p>' +
                                   '</div>'+
                                   '<hr>'
                                '</div>';
              
                 var currentElement =  $(angular.element($event.currentTarget));
                // $(angular.element(currentElement)).closest('.modal-footer').appendChild("<h1>Hello world</h1>");
                 
                  $(angular.element(currentElement)).closest('.modal-footer').append(cmtChild);
                 //var dataID =  $(angular.element(currentElement)).closest('.modal-footer').attr('data-id');
                 //alert(dataID);
                 //alert($(angular.element(currentElement)).closest('.modal-footer').attr('data-id')  );
             }
         });
     }
     
     
     /*
        like image
     */
     
     $scope.deletePic = function($event, img_id) {
         
         url = '/deletePic?imgID=' + img_id;
         console.log('imgID = ' + img_id);
         $.ajax({
             url: url,
            imgID: img_id,
            success: function(data){
                alert("You have sucessfully deleted this photo.");
                location.reload();
            }
        });
     }
     
     $scope.handleLike = function($event, img_id){
         
         var item =  $(angular.element($event.currentTarget));
         var url;

         var likeCount = item.prev('p').text();
         if(!(parseInt(likeCount) >= 0)){
            likeCount='0';
         }
         
         
         if(item.hasClass('heart-unfilled'))    // like image
         {
            url = '/addLike?photo_id=' + img_id;
            $(angular.element(item)).removeClass('heart-unfilled'); 
            $(angular.element(item)).addClass('heart-filled'); 
            item.prev('p').html(parseInt(likeCount)+1);
         }else{                                 // unlike image
            url = '/unlike?photo_id=' + img_id;
            $(angular.element(item)).removeClass('heart-filled'); 
            $(angular.element(item)).addClass('heart-unfilled'); 
            item.prev('p').html(parseInt(likeCount)-1);
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


     /*
        load right panel that shows clothing item info
     */
     $scope.loadClothingPanel = function($event, img_id, img_url){
            var item = $event.currentTarget;

            // hide all photos and show the photo clicked
            $scope.showAllPhotos = false;

            // replace image in photo section
            $scope.select_image_url = img_url;

            $.ajax({
                url: '/getItems?imgID=' + img_id,
                success: function(data){
                    $scope.items = [];

                    data = JSON.parse(data);
                    data = data['result'];

                   // printJSON(data);


                    for(var i=0; i<data.length; i++){
                        data[i].title = data[i].clothingType;
         
                        $scope.$apply(function(){
                            $scope.items.push(data[i]);
                        });
                    }
                }
            });
     }

     /*
        outline item on photo
     */
     $scope.viewItem = function($event){

        var item = $event.currentTarget;
        var x1 = $(angular.element(item)).attr('data-x1'); 
        var x2 = $(angular.element(item)).attr('data-x2');
        var y1 = $(angular.element(item)).attr('data-y1'); 
        var y2 = $(angular.element(item)).attr('data-y2');
        var title = $(angular.element(item)).attr('data-title');

        $('#itemPopUp').css('top', (y1-20)+'px');
        $('#itemPopUp').css('left', x1+'px');
        $('#itemPopUp').html(title);

        $('#itemPhoto').imgAreaSelect({ x1: x1, y1: y1, x2: x2, y2: y2, movable:false, resizable:false, outerOpacity: 0.4});
     }


     /*
        hide image items and show gallery
     */
     $scope.showGallery = function(){
        $('#itemPhoto').imgAreaSelect({
            hide: true
        });
        $('#itemPopUp').html('');

     }
     
     $scope.populateAll = function() {
         //console.log("populating all");
         $scope.showAdoredOnly = false;
         $scope.images = [];
         $scope.reloadImages();
     }
     
     $scope.populateAdored = function() {
         //console.log("populating adored");
         $scope.showAdoredOnly = true;
         $scope.images = [];
         $scope.reloadImages();
     }
     
     $scope.reloadImages = function() {

         $.ajax({
           
        url: '/getPhotosJSON?user_id=' + 1 + '&page=' + page + '&adored=' + $scope.showAdoredOnly,
        data: {},
        dataType: 'json',

        success: function(data){
            //console.log(data);

            var page_url = window.location.href;
            var isProfilePage = false, isGalleryPage = false;
            
            if(page_url.indexOf("profile") > -1){
                isProfilePage = true;
            }else if(page_url.indexOf("gallery") > -1){
                isGalleryPage = true;
            }
            
            var photosLength;   // amount of photos to load
            
            // if current page contains '#homeCarousel' then the current page must be the index
            if( $('#homeCarousel').length > 0 && data.length>=15){
                photosLength = 15;
            }else{
                photosLength = data.length;
            }
                        
           // alert(JSON.stringify(data, null, 2));
            
            for( var i = 0; i < photosLength; i++ ) {
   
                var likes;
                
                if(data[i].total_likes == 0){
                    likes = '';
                }else{
                    likes = data[i].total_likes;
                }
                
                
                var img = {
                    'profilePage': isProfilePage,
                    'galleryPage': isGalleryPage,
                    'image_url': data[i].image_url,
                    'img_id': data[i].img_id,
                    'title': data[i].title,
                    'adored': data[i].adored,
                    'comments': data[i].comments,
                    'deleteOption': data[i].deleteOption,
                    'profilePicOption': data[i].profilePicOption,
                    'total_likes': likes
                };
                
               
                $scope.populateGallery(img);               
            
            }
        },
        error: function ( jqXHR, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
     }
     
     
    $scope.categories = [];
     $scope.loadOption = function(){
          $scope.categories.push('Chic', 'Finals', 'Parisian', 'Lazy Day', 'Pitt Spirit', 'Cool', 'Elegant', 'Tomboy', 'Metal', 'Bro', 'Halloween', 'Goofy', 'Comfortable', 'High Fashion', 'British', 'Conservative', 'Sexy');
     }
     

});






















