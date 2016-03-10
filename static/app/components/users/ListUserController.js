(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('ListUserController', ListUserController);

  ListUserController.$inject = ['userUtils'];

  function ListUserController(
    userUtils
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
          name: 'Gary Busey',
          email: 'busey@mail.com',
          status: 0
        },
        {
          name: 'Gary Busey',
          email: 'busey@mail.com',
          status: 1
        },
        {
          name: 'Gary Busey',
          email: 'busey@mail.com',
          status: 0
        }
      ];
      vm.totalItems = vm.users.length;
    }

  }

}());