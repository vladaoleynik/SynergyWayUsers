(function () {
  'use strict';

  angular.module('synergyWayUsers')
    .directive('menuBar', menuBar);

  function menuBar($location) {
    return {
      restrict: 'E',
      templateUrl: '/synergyWayUsers/app/static/js/app/shared/menu-bar/menu-bar.html',
      link: function(scope, element, attrs) {
        scope.menuClass = menuClass;

        function menuClass(page) {
          var current = $location.path().substring(1);
          return page === current ? "active" : "";
        }
      }
    };
  }
})();