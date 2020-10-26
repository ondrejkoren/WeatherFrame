import { BodyController } from './controllers/body.controller.js';
import { AsyncButtonComponent } from './components/async-button/async-button.component.js';
import { FileInputDirective } from './directives/file-input.directive.js';

const WeatherStationWebUIApp = "WeatherStationWebUIApp";
let app = angular.module(WeatherStationWebUIApp, []);

// Controllers
app.controller("BodyController", BodyController);

// Components
app.component(AsyncButtonComponent.name, AsyncButtonComponent);

// Directives
app.directive('fileInput', FileInputDirective);

// Config
let interpolateConfig = function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
}
interpolateConfig.$inject = ["$interpolateProvider"];
app.config(interpolateConfig);

export { WeatherStationWebUIApp };
