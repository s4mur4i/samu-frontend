var samu = angular.module('samu', ["ngCookies"]);

samu.controller('SamuCtrl', function SamuCtrl($scope, $http, $cookies, $window) {

    $scope.set_error = function(err_msg) {
        $scope.error = true;
        $scope.error_msg = err_msg;
    }

    $scope.clear_error = function() {
        $scope.error = false;
    }

    $scope.login = function() {
       var post_data = "username="+$scope.username+"&password="+$scope.password;
       post_data = { username: $scope.username, password: $scope.password };
       $http.post("/login", post_data).success(
          function(data, status, headers, config) {
              if (data.success === true)
                {
                  $window.location.href = '/welcome';
                  $scope.clear_error();
                }
              else
                {
                  $scope.set_error("Login failed!");
                }
          }
       );
    };
});
