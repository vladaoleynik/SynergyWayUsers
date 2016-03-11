(function () {
  'use strict';

  angular.module('synergyWayUsers')
    .directive('convertToNumber', convertToNumber)
    .directive('includeReplace', includeReplace);

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