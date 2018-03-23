const path = require('path');
const fs = require('fs');

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database(path.join(__dirname, './data/data.db'));

function __insertDB(disData) {
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
}

function importDis() {
  const oldDis = path.join(__dirname, './data/dis.dat');
  fs.readFile(oldDis, 'utf8', (err, data) => {
    if(err) {
      return ;
    }

    let disData = JSON.parse(data);
    __insertDB(disData);
  });
}

function daulDis() {
}

function main() {
  if(process.argv.length < 3) {
    console.log("Usage: node tools.js [import|daul]");
    process.exit(1);
  }
  
  if(process.argv[2] == "import") {
    importDis();
  } else if(process.argv[2] == "daul") {
    daulDis();
  } else {
    console.log("Usage: node tools.js [import|daul]");
    process.exit(1);
  }
}

main();

