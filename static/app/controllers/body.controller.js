var BodyController = function($scope, $http) {

    $scope.uiStates = {
        refreshing: false
    };

    $scope.screens = [
        { name: "Ring Screen", type: "ringscreen" },
        { name: "Quadrant Screen", type: "quadrantscreen" }
    ];

    $scope.imageUrl = "";
    $scope.displayImageUrl = "";

//    $scope.file = [];

    $scope.refresh = function() {
        $scope.uiStates.refreshing = true;
        $http.get("/api/refresh").then(r => {
            console.log("Response: ", r);
        })
        .finally(() => {$scope.uiStates.refreshing = false;});
    };

    $scope.uploadImage = function() {
        let formData = new FormData();
        formData.append('file', $scope.file[0]);
        console.log("$scope.file: ", $scope.file);
        $http.post('/api/uploadImage', formData, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .then(success => {
            console.log("Success: ", success);
            $scope.imageUrl = "/api/getimage/" + success.data.imageUrl;
            $scope.displayImageUrl = "/api/display/" + success.data.imageUrl;
            console.log("image url: ", $scope.imageUrl);
            console.log("$scope.displayImageUrl: ", $scope.displayImageUrl);
        }, error => {
            console.error("Error: ", error);
        });
    };

    $scope.displayLastImage = function() {
        $scope.uiStates.refreshing = true;
        $http.get($scope.displayImageUrl)
        .then(res => console.log("res: ", res), err => console.error("err: ", err))
        .finally(() => $scope.uiStates.refreshing = false);
    }

    this.$onInit = function() {
        console.log("BodyController $onInit()");
    };
}

BodyController.$inject = ["$scope", "$http"];

export { BodyController };
