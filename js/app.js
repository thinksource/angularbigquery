'use strict';


// Declare app level module which depends on filters, and services
var app = angular.module('myapp', ['ngTouch', 'ui.grid','ui.router']).config(function ($stateProvider, $urlRouterProvider)  {

    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'views/home/home.html',
        controller: 'MainCtrl'
      });

    $urlRouterProvider.otherwise('/');
  });