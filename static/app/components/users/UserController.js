(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('UserController', UserController);

  UserController.$inject = [];

  function UserController() {
    var vm = this;

    vm.model = undefined;
    vm.totalItems = 50;
    vm.currentPage = 1;

    activate();

    function activate() {

    }

  }

}());