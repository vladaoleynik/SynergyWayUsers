(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('ListUserController', ListUserController);

  ListUserController.$inject = ['userUtils', 'userService'];

  function ListUserController(
    userUtils,
    userService
  ) {
    var vm = this;

    vm.users = [];

    vm.itemsPerPage = 15;
    vm.totalItems = 0;
    vm.currentPage = 1;

    vm.formatUserStatus = userUtils.formatUserStatus;

    vm.loadPaginatedUsers = loadPaginatedUsers;

    activate();

    function activate() {
      loadPaginatedUsers();
    }

    function loadPaginatedUsers() {
      userService.query({page: vm.currentPage, number: vm.itemsPerPage})
        .$promise
        .then(userSuccess)
        .catch(userError);

      function userSuccess(response) {
        vm.users = response;
        if(vm.users.length)
          vm.totalItems = vm.users[0].full_count;
        else
          vm.totalItems = 0
      }

      function userError() {

      }
    }

  }

}());