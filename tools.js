const path = require('path');
const fs = require('fs');

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database(path.join(__dirname, './data/data.db'));
const oldDis = path.join(__dirname, './data/dis.dat');

function importDis() {
  fs.readFile(oldDis, 'utf8', (err, data) => {
    if(err) {
      return ;
    }

    let disData = JSON.parse(data);
    db.serialize(() => {
      db.run("CREATE TABLE IF NOT EXISTS distance (src TEXT, dst TEXT, dis FLOAT)");
      
      let stmt = db.prepare("INSERT INTO distance VALUES (?, ?, ?)");
      for(let i=0; i<disData.length; ++i) {
        stmt.run(disData[i][0], disData[i][1], disData[i][2]);
      }
      console.log(`Start insert ${disData.length} records.`);
      stmt.finalize();
      console.log(`Finish insert records.`);
      
      db.get("SELECT COUNT(*) FROM distance", (err, row) => {
        console.log(`Finish insert ${row} records.`);
      });
    });
  });
}

function main() {
  importDis();
}

main();

