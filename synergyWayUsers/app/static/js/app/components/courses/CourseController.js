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
        if (response.status == 'error') {
          courseError();
          return;
        }

        vm.courses = response;
        vm.successfulRequest = true;
      }

      function courseError() {
        vm.successfulRequest = false;
      }
    }

  }

}());