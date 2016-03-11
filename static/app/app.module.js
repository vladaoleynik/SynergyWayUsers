(function () {

  'use strict';

  angular
    .module('synergyWayUsers', [
      'ui.router',
      'ui.bootstrap',
      'ui.mask',
      'ngMessages'
    ])
    .config([
      appConfig
    ])
    .run(runFunction);

  function appConfig() {

  }

  function runFunction($rootScope, $state, $stateParams) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
  }

})();

