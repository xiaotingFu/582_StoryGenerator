const sqlite3 = require('sqlite3').verbose();
var express = require('express');
var router = express.Router();
const path = require('path')
const dbPath = path.resolve(__dirname, '../../db/db.sqlite3')

function get_bookcontent(book1, book2, res){
    //connect to database
    var arr = [];
    var dict = {};
    let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
          console.error(err.message);
        }
        console.log('Connected to the story database.');
      }); 
    
      db.each(`SELECT title, url from Story where book1='${book1}' AND book2='${book2}'`, (err, row) => {
        if (err) {
          console.error(err.message);
        }
        //console.log(row.title + "\t" + row.url);
	if (Object.keys(dict).length < 1){
	dict[row.title]=row.url;
	}
	 
        arr.push(row.url);
      }); 
    db.close((err) => {
        if (err) {
          console.error(err.message);
        } 
        console.log(dict);
        console.log('Close the database connection.'); 
        res.send(dict);
    });  
} 

/* GET users listing. */
router.get('/', function(req, res, next) {
    var book1 = req.query.book1;
    var book2 = req.query.book2;
    get_bookcontent(book1, book2 , res); 
});

module.exports = router;
