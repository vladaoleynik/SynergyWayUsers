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
        templateUrl: '/synergyWayUsers/app/static/js/app/components/user-list/user-list.html'
      })
      .state('edit-user', {
        url: '/users/{userId:int}/edit',
        controller: 'SingleUserController as vm',
        templateUrl: '/synergyWayUsers/app/static/js/app/components/user/edit-user.html'
      })
      .state('create-user', {
        url: '/users/new',
        controller: 'SingleUserController as vm',
        templateUrl: '/synergyWayUsers/app/static/js/app/components/user/create-user.html'
      })
      .state('courses', {
        url: '/courses',
        controller: 'CourseController as vm',
        templateUrl: '/synergyWayUsers/app/static/js/app/components/courses/courses.html'
      })
  }

})();

