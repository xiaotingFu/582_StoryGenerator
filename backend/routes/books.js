const sqlite3 = require('sqlite3').verbose();
var express = require('express');
var router = express.Router();
const path = require('path');
const dbPath = path.resolve(__dirname, '../../db/db.sqlite3');
var fs = require("fs");
/**
 * Test POST
book1:Harry Potter
book2:Hobbit
romance:2
cliche:3
horror:5
boring:2
violence:1
 */

 //Backend support CORS
class Story {

  constructor(book1, book2) {
    this.book1 = book1;
    this.book2 = book2;
    this.romance = 1;
    this.cliche = 1;
    this.horror = 1;
    this.boring = 1;
    this.violence = 1;
    this.url = [];
  }

}
/**
     * Given a story content 
     * Get the story url and send the data to the generator
     * Save the temp data to a json file
     */
function get_bookcontent(story, res) {
  //connect to database
  let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the story database.');
  });

  db.each(`SELECT url from Summary where book1='${story.book1}' AND book2='${story.book2}'`, (err, row) => {
    if (err) {
      console.error(err.message);
    }
    //update the url to be the summary url
    story.url = row.url;
  });
  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Close the database connection.');
    fs.writeFile("../db/tmp.json", JSON.stringify(story), (err) => {
      if (err) {
        console.error(err);
        return;
      };
      console.log("JSON file has been created/updated!");
    });
    //a dictionary
    const { spawn } = require('child_process');
    // const pyprog = spawn('python', ['../gen_backend/story_preprocess.py']);
    const pyprog = spawn('python', ['../gen_backend/final_story.py']);
    pyprog.stdout.on('data', function (data) {
        //console.log(data.toString());
        // var storyfile = '../db/output.txt';
        var story_content = data;
        // fs.readFile(storyfile, function read(err, data) {
        //     if (err) {
        //         throw err;
        //     }
        //     story_content = data;
        // });
        console.log(story_content.toString())
        var sendfile = {"story": story_content.toString()};
        res.send(JSON.stringify(sendfile));
        res.end('end');
    });
  });
}

/* GET books listing. */
router.get('/', function (req, res, next) {
  var story = new Story(req.query.book1, req.query.book2)
  story.romance = req.query.romance;
  story.cliche = req.query.cliche;
  story.horror = req.query.horror;
  story.boring = req.query.boring;
  story.violence = req.query.violence;
  get_bookcontent(story, res);
});

module.exports = router;
