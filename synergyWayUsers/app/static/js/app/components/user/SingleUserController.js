(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('SingleUserController', SingleUserController);

  SingleUserController.$inject = [
    '$stateParams', '_', 'userService', 'courseService', '$state', '$timeout'
  ];

  function SingleUserController(
    $stateParams,
    _,
    userService,
    courseService,
    $state,
    $timeout
  ) {
    var vm = this;

    vm.model = {
      status: 1
    };
    vm.inEditView = true;
    vm.successfulRequest = undefined;

    vm.allCourses = [];

    vm.selectedCourse = undefined;
    vm.selectCourse = selectCourse;
    vm.addCourse = addCourse;
    vm.removeCourse = removeCourse;
    vm.getAvailableCourses = getAvailableCourses;

    vm.updateUser = updateUser;
    vm.createUser = createUser;

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

        if (vm.model.status)
          vm.model.status = 1;
        else
          vm.model.status = 0;

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

    function prepareUserData() {
      var data = {
        course_ids: [],
        email: vm.model.email,
        user_id: vm.model.id,
        mobile: vm.model.mobile,
        name: vm.model.name,
        phone: vm.model.phone,
        status: Boolean(vm.model.status)
      },
        course_ids = [];

      _.forEach(vm.model.courses, function(item) {
        course_ids.push(item.course_id);
      });

      data.course_ids = course_ids;

      return data;
    }

    function updateUser(){
      var data = prepareUserData();

      vm.successfulRequest = undefined;

      userService.update({userId: vm.model.id}, data)
        .$promise
        .then(userSuccess)
        .catch(userError);

      function userSuccess(response) {
        if (response.status == 'error') {
          userError();
          return;
        }

        vm.successfulRequest = true;
        $timeout(function () {
          $state.go('user-list');
        }, 3000)

      }

      function userError() {
        vm.successfulRequest = false;
      }
    }

    function createUser(){
      var data = prepareUserData();

      vm.successfulRequest = undefined;

      userService.save(data)
        .$promise
        .then(userSuccess)
        .catch(userError);

      function userSuccess(response) {
        if (response.status == 'error') {
          userError();
          return;
        }

        vm.successfulRequest = true;
        $timeout(function () {
          $state.go('user-list');
        }, 3000)

      }

      function userError() {
        vm.successfulRequest = false;
      }
    }

  }

}());