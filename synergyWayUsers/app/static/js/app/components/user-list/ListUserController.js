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

    vm.search = undefined;
    vm.successfulRequest = undefined;

    vm.itemsPerPage = 15;
    vm.totalItems = 0;
    vm.currentPage = 1;

    vm.formatUserStatus = userUtils.formatUserStatus;

    vm.loadPaginatedUsers = loadPaginatedUsers;
    vm.deleteUser = deleteUser;

    activate();

    function activate() {
      loadPaginatedUsers();
    }

    function loadPaginatedUsers() {
      userService.get({
        page: vm.currentPage,
        number: vm.itemsPerPage,
        search_str: vm.search
      })
        .$promise
        .then(userSuccess)
        .catch(userError);

      function userSuccess(response) {
        if (response.status == 'error') {
          userError();
          return;
        }

        vm.users = response.data;
        vm.totalItems = response.count;

        vm.successfulRequest = true;
      }

      function userError() {
        vm.successfulRequest = false;
      }
    }

    function deleteUser(userId) {
      userService.delete({userId: userId})
        .$promise
        .then(userSuccess)
        .catch(userError);

      function userSuccess(response) {
        var index = _.findIndex(vm.users, {id: userId});
        if (index > -1)
          vm.users.splice(index, 1);

        vm.successfulRequest = true;
      }

      function userError(error) {
        vm.successfulRequest = false;
      }
    }

  }

}());