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

app.get('/report/:id', function (rq, res){
    // route to the report for an id 
    res.send('report' + rq.params.id)
})

app.post('/api/', function (rq, res){
    res.send('hello workd')
})


app.listen(3000, function (){
    console.log('listening on port 3000')
})
