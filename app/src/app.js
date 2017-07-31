var Backbone = require('backbone')
// Bootstrap wants jQuery global
window.jQuery = $ = require('jquery')
var bootstrap = require('bootstrap')
require('../css/style.css')
console.log(bootstrap)

var answers; // hold the answers

// our user interface is built on quesitons
var Question = Backbone.Model.extend({
    idAttribute: 'question_id'
})


var Questions = Backbone.Collection.extend({
    model: Question,
    // the collection of questions
    url: '/questions/'
})


var Section = Backbone.Model.extend({
    // questions come in sections - not sure we need this level
})

var questions = new Questions();
questions.fetch()

console.log(questions)

// Todo:
// we
