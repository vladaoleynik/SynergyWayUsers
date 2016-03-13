(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('CourseController', CourseController);

  CourseController.$inject = [];

  function CourseController() {
    var vm = this;

    vm.courses = [];

    activate();

    function activate() {
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
    }

  }

}());