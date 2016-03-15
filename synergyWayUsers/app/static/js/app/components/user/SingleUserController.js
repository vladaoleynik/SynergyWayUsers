(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('SingleUserController', SingleUserController);

  SingleUserController.$inject = [
    '$stateParams', '_', 'userService', 'courseService'
  ];

  function SingleUserController(
    $stateParams,
    _,
    userService,
    courseService
  ) {
    var vm = this;

    vm.model = {
      status: 1
    };
    vm.inEditView = true;

    vm.allCourses = [];

    vm.selectedCourse = undefined;
    vm.selectCourse = selectCourse;
    vm.addCourse = addCourse;
    vm.removeCourse = removeCourse;
    vm.getAvailableCourses = getAvailableCourses;

    activate();

    function activate() {
      var userId = $stateParams.userId;

      vm.inEditView = Boolean(userId);

      courseService.query()
        .$promise
        .then(courseSuccess)
        .catch(courseError);

      function courseSuccess(response) {
        vm.allCourses = response;

        selectCourse(0);
      }

      function courseError() {

      }

      if (userId) {
        userService.get({userId: userId})
          .$promise
          .then(userSuccess)
          .catch(userError);
      }

      function userSuccess(response) {
        vm.model = response;

        selectCourse(0);
      }

      function userError() {

      }
    }

    function addCourse(dataList, item) {
      dataList.push(item);
      selectCourse(0);
    }

    function removeCourse(dataList, item) {
      var index = _.indexOf(dataList, item);

      if (index == -1)
        return;

      dataList.splice(index, 1);
      selectCourse(0);
    }

    function selectCourse(index) {
      vm.selectedCourse = getAvailableCourses()[index];
    }

    function getAvailableCourses() {
      return _.filter(vm.allCourses, function(obj){
        return !_.find(vm.model.courses, obj);
      });
    }

  }

}());