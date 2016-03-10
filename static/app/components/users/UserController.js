(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('UserController', UserController);

  UserController.$inject = ['$scope'];

  function UserController($scope) {
    var vm = this;

    $scope.model = {
      status: 0
    };

    vm.totalItems = 50;
    vm.currentPage = 1;

    activate();

    function activate() {

    }

  }

}());