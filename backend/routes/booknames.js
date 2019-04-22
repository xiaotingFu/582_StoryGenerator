const sqlite3 = require('sqlite3').verbose();
var express = require('express');
var router = express.Router();
const path = require('path');
const dbPath = path.resolve(__dirname, '../../db/db.sqlite3');
var fs = require("fs");

function getBooknames(res, bookname){
    var booknames = [];
    let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
          console.error(err.message);
        }
        console.log('Connected to the summary database.');
      });
      var sql = `SELECT DISTINCT(book2) from Summary where book1='${bookname}'`
      db.each(sql, (err, row) => {
        if (err) {
          console.error(err.message);
        }
        booknames.push(row.book2);
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
    var bookname = req.query.bookname; // book name
    getBooknames(res, bookname);
  });

module.exports = router;

