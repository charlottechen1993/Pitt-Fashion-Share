

var angularAPP = angular.module('angular-app', []);

/* replace braces so that html interprets brackets as angularjs code*/
angularAPP.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);



function printJSON(json){
    alert(JSON.stringify(json, null, 2));
    console.log(JSON.stringify(json, null, 2));
}
