(function () {

  'use strict';

  angular
    .module('synergyWayUsers')
    .config([
      '$stateProvider',
      '$urlRouterProvider',
      routeConfig
    ]);

  function routeConfig($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/users");

    $stateProvider
      .state('user-list', {
        url: '/users',
        controller: 'UserController',
        templateUrl: 'components/users/user-list.html'
      })
      .state('single-user', {
        url: '/users/{campaignId:int}/edit',
        controller: 'UserController',
        templateUrl: 'components/users/single-user.html'
      })
      .state('courses', {
        url: '/courses',
        controller: 'CourseController',
        templateUrl: 'components/courses/courses.html'
      })
  }

})();

