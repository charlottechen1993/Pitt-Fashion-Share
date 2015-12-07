 angularAPP.controller('profileController', function($scope,$http){
     $scope.categories = [];
     $scope.loadOption = function(){
//          $scope.$apply(function(){
//            $scope.categories.push(['Chic', 'Funny', 'Finals', 'Lazy', 'Parisian']);
              $scope.categories.push('Chic');
//        });
     }
 });
                       