(function () {

  angular
    .module('synergyWayUsers')
    .factory('userService', userService);

  userService.$inject = ['$resource'];
  function userService($resource) {
    return $resource('/api/users')
  }

})();