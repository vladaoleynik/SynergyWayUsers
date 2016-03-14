(function () {

  angular
    .module('synergyWayUsers')
    .factory('userService', userService)
    .factory('courseService', courseService);

  userService.$inject = ['$resource'];
  function userService($resource) {
    return $resource('/api/users')
  }

  courseService.$inject = ['$resource'];
  function courseService($resource) {
    return $resource('/api/courses')
  }

})();