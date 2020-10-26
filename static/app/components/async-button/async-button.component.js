function AsyncButtonController($log) {
    "use strict";

    var $ctrl = this;

    $ctrl.$onInit = function() {
    };

    $ctrl.nop = function () { };
}

AsyncButtonController.$inject = ["$log"];

const AsyncButtonComponent = {
    templateUrl: "/static/app/components/async-button/async-button.component.html",
    bindings: {
        loading: '=',
        stateActive: '@',
        stateInactive: '@',
        overrideClass: '@?',
        disabled: '=?',
        longDisabledString: '=?',             // can't use "disabled" for long strings since it is restricted to 127 characters in Microsoft Edge
        disabledReason: '@?',
        disabledIncludeSpinner: '=?'
    },
    controller: AsyncButtonController,
    transclude: true,
    name: "asyncButton"
};

//cost AsyncButtonComponentName = "asyncButton";

export { AsyncButtonComponent };
