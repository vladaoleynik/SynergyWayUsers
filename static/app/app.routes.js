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
        controller: 'UserController as vm',
        templateUrl: '/static/app/components/users/user-list.html'
      })
      .state('single-user', {
        url: '/users/{campaignId:int}/edit',
        controller: 'UserController as vm',
        templateUrl: '/static/app/components/users/single-user.html'
      })
      .state('courses', {
        url: '/courses',
        controller: 'CourseController as vm',
        templateUrl: '/static/app/components/courses/courses.html'
      })
  }

})();

