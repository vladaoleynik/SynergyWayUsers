(function () {
  'use strict';

  angular.module('synergyWayUsers')
    .directive('menuBar', menuBar)
    .directive('convertToNumber', convertToNumber)
    .directive('includeReplace', includeReplace);

  function menuBar($location) {
    return {
      restrict: 'E',
      templateUrl: '/static/app/shared/menu-bar/menu-bar.html',
      link: function(scope, element, attrs) {
        scope.menuClass = menuClass;

        function menuClass(page) {
          var current = $location.path().substring(1);
          return page === current ? "active" : "";
        }
      }
    };
  }

  function convertToNumber() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, ngModel) {
        ngModel.$parsers.push(function(val) {
          return parseInt(val, 10);
        });
        ngModel.$formatters.push(function(val) {
          return '' + val;
        });
      }
    };
  }

  function includeReplace() {
    return {
        require: 'ngInclude',
        restrict: 'A', /* optional */
        link: function (scope, el, attrs) {
            el.replaceWith(el.children());
        }
    };
  }

})();