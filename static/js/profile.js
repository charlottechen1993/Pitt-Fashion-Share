 angularAPP.controller('profileController', function($scope,$http){
     $scope.categories = [];
     $scope.loadOption = function(){
          $scope.categories.push('Chic', 'Finals', 'Parisian', 'Lazy Day', 'Pitt Spirit', 'Cool', 'Elegant', 'Tomboy', 'Metal', 'Bro', 'Halloween', 'Goofy', 'Comfortable', 'High Fashion', 'British', 'Conservative', 'Sexy');
     }
     
     $scope.categories = [];
     $scope.loadOption = function(){
          $scope.categories.push('Chic', 'Finals', 'Parisian', 'Lazy Day', 'Pitt Spirit', 'Cool', 'Elegant', 'Tomboy', 'Metal', 'Bro', 'Halloween', 'Goofy', 'Comfortable', 'High Fashion', 'British', 'Conservative', 'Sexy');
     }
     
     $scope.selected = [];
 });
                       