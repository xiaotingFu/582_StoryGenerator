const sqlite3 = require('sqlite3').verbose();
var express = require('express');
var router = express.Router();
const path = require('path');
const dbPath = path.resolve(__dirname, '../../db/db.sqlite3');
var fs = require("fs");

function getBooknames(res){
    var booknames = [];
    let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
          console.error(err.message);
        }
        console.log('Connected to the story database.');
      });
    
      db.each(`SELECT DISTINCT(book1) from Story`, (err, row) => {
        if (err) {
          console.error(err.message);
        }
        booknames.push(row.book1);
      });
      db.close((err) => {
        if (err) {
          console.error(err.message);
        }
        console.log(booknames);
        console.log('Close the database connection.');
        res.send(JSON.stringify(booknames))
      });

}
router.get('/', function (req, res, next) {

    res.send()
  });