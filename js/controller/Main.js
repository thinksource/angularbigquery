'use strict';



app.controller('MainCtrl', ['$scope', '$http', function ($scope, $http) {

    $scope.sql={query:"SELECT area_codes,timezone, primary_city,longitude,estimated_population, latitude, county FROM [testdata.zip_code] LIMIT 1000"}
    $scope.bgquery=function(){
        alert(this.sql.query);
        $scope.gridOptions.data={}
        $http.post('json', this.sql)
            .success(function(data) {
        for( var i=0; i<5; i++) {
            data = data.concat(data);
        }
      $scope.errormessage="";
      $scope.gridOptions.data = data;
    }).error(function(error){
                //var jsonobj=JSON.parse(error);

                $scope.errormessage=error.message;
            });
    }
    $scope.gridOptions = {
        enableFiltering: false
    };
    $scope.reset=function(){
        $scope.sql={query:"SELECT area_codes,timezone, primary_city,longitude,estimated_population, latitude, county FROM [testdata.zip_code] LIMIT 1000"};
    }
  //$scope.gridOptions.columnDefs = [
  //    {name:'zip'},
  //    {name:'longitude'},
  //    {name:'state'},
  //    {field:'latitude'}, // showing backwards compatibility with 2.x.  you can use field in place of name
  //    {name: 'city', field: 'primary_city'}
  //
  //];

  $http.get('/json')
  //$http.get('sqlitedata')
    .success(function(data) {
      for( var i=0; i<5; i++){
        data = data.concat(data);
      }
      $scope.errormessage="";
      $scope.gridOptions.data = data;
    });
}]);