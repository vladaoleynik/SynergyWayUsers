(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('SingleUserController', SingleUserController);

  SingleUserController.$inject = ['$stateParams'];

  function SingleUserController(
    $stateParams
  ) {
    var vm = this;

    vm.model = {
      id: 1,
      name: 'Gary Busey',
      email: 'busey@mail.com',
      phone: '380678625609',
      status: 1
    };
    vm.inEditView = true;

    vm.courses = [
      {
        id: 1,
        name: 'Python-Base',
        code: 'P012346'
      },
      {
        id: 2,
        name: 'Python-DataBase',
        code: 'P012347'
      },
      {
        id: 3,
        name: 'HTML',
        code: 'P012348'
      }
    ];

    activate();

    function activate() {
      var userId = $stateParams.userId;

      vm.inEditView = Boolean(userId);

    }

  }

}());