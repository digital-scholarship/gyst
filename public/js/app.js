
// our user interface is built on quesitons
var Question = Backbone.Model.extend({
    // stuff in here
})


var Questions = Backbone.Collection.extend({
    // the collection of questions
    url: '/questions'
})


var Section = Backbone.model.extend({
    // questions come in sections - not sure we need this level
})

var quesitons = new Questions;

console.log(questions)


