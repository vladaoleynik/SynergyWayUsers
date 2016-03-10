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
        controller: 'ListUserController as vm',
        templateUrl: '/static/app/components/users/user-list.html'
      })
      .state('edit-user', {
        url: '/users/{campaignId:int}/edit',
        controller: 'SingleUserController as vm',
        templateUrl: '/static/app/components/users/single-user.html'
      })
      .state('create-user', {
        url: '/users/new',
        controller: 'SingleUserController as vm',
        templateUrl: '/static/app/components/users/single-user.html'
      })
      .state('courses', {
        url: '/courses',
        controller: 'CourseController as vm',
        templateUrl: '/static/app/components/courses/courses.html'
      })
  }

})();

