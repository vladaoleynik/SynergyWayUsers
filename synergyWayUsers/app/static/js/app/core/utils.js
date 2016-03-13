(function() {
  'use strict';

  angular
    .module('synergyWayUsers')
    .service('userUtils', userUtils);

  function userUtils() {
    return {
      formatUserStatus: formatUserStatus
    };

    function formatUserStatus(index) {
      if (index)
        return 'Active';

      return 'Inactive';
    }
  }


}());