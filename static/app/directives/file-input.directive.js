let FileInputDirective = function($parse) {
    return {
        restrict: 'A',
        link: function(scope, elm, attrs) {
            elm.bind('change', function() {
                console.log("elm[0].file: ", elm[0].files);
                $parse(attrs.fileInput).assign(scope, elm[0].files);
                scope.$apply();
                console.log("scope: ", scope);
                console.log("elm: ", elm);
                console.log("attrs: ", attrs);
            })
        }
    };
}

FileInputDirective.$inject = ["$parse"];

export { FileInputDirective };
