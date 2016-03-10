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
          name: 'Python-Base',
          code: 'P012345'
        },
        {
          name: 'Python-DataBase',
          code: 'P012345'
        },
        {
          name: 'HTML',
          code: 'P012345'
        }
      ];
    }

  }

}());