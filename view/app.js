var express = require('express');
var app = express();
var port = (process.argv[2] || 3000);

app.use('/', express.static(__dirname + '/public'));
app.use('/logs', express.static(__dirname + '/logs'));

var server = app.listen(port, function(){
	console.log('Listening on port %d', port);
})