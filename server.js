const express = require('express' );
const app = express();
const bodyParser = require('body-parser');
const base58 = require('./base58.js');
const path = require('path');

app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', function (rq, res){
    // route to the homepage index.html
    res.send('hello workd')
})

app.get('/result/:id', function (rq, res){
    // route to the report for an id 
    res.send('report' + rq.params.id)
})

app.get('/questions', function(rq, res){
    res.sendFile(__dirname + '/public/questions/dobject.json');
})


app.get('/stats', function (rq, res){
    // route to fetch and return stats - global average for each qn and country averages
    res.send('stats')
})


app.post('/result', function (rq, res){
    res.send('hello workd')
        console.log('received : ' + rq.params)

        // we will call the geoip service and store country
        // a result will have an id, a base58 for short url, country, and answers
})


app.listen(8080, function (){
    console.log('listening on port 8080')
})
