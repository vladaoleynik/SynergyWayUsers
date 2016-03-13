(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('ListUserController', ListUserController);

  ListUserController.$inject = ['userUtils', '$state'];

  function ListUserController(
    userUtils,
    $state
  ) {
    var vm = this;

    vm.users = [];

    vm.itemsPerPage = 15;
    vm.totalItems = 0;
    vm.currentPage = 1;

    vm.formatUserStatus = userUtils.formatUserStatus;

    activate();

    function activate() {
      vm.users = [
        {
          id: 1,
          name: 'Gary Busey',
          email: 'busey@mail.com',
          status: 0
        },
        {
          id: 2,
          name: 'Gary Busey',
          email: 'busey@mail.com',
          status: 1
        },
        {
          id: 3,
          name: 'Gary Busey',
          email: 'busey@mail.com',
          status: 0
        }
      ];
      vm.totalItems = vm.users.length;
    }

  }

}());