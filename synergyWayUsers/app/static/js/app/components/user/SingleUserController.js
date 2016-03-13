(function(){
  'use strict';

  angular
    .module('synergyWayUsers')
    .controller('SingleUserController', SingleUserController);

  SingleUserController.$inject = [
    '$stateParams', '_'
  ];

  function SingleUserController(
    $stateParams,
    _
  ) {
    var vm = this;

    vm.model = {
      status: 1
    };
    vm.inEditView = true;

    vm.allCourses = [
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

    vm.selectedCourse = undefined;
    vm.selectCourse = selectCourse;
    vm.addCourse = addCourse;
    vm.removeCourse = removeCourse;
    vm.getAvailableCourses = getAvailableCourses;

    activate();

    function activate() {
      var userId = $stateParams.userId;

      vm.inEditView = Boolean(userId);

      if (userId) {
        vm.model = {
          id: 1,
          name: 'Gary Busey',
          email: 'busey@mail.com',
          phone: '380678625609',
          status: 1,
          courses: [
            {
              id: 1,
              name: 'Python-Base',
              code: 'P012346'
            }
          ]
        };

      }

      selectCourse(0);
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