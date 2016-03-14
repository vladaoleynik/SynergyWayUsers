(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('CourseController', CourseController);

  CourseController.$inject = [
    'courseService'
  ];

  function CourseController(
    courseService
  ) {
    var vm = this;

    vm.courses = [];

    activate();

    function activate() {
      courseService.query()
        .$promise
        .then(courseSuccess)
        .catch(courseError);

      function courseSuccess(response) {
        vm.courses = response;
      }

      function courseError() {

      }
    }

  }

}());