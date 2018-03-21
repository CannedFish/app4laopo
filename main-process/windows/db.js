const path = require('path');
const ipc = electron.ipcMain;

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database(path.join(__dirname, '../../data/data.db'));

exports.createTable = () => {
  db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS distance (src TEXT, dst TEXT, dis FLOAT)");
  });
}

exports.insertDistance = (dis) => {
  db.serialize(() => {
    let stmt = db.prepare("INSERT INTO distance VALUES (?, ?, ?)");
    dis.map((_d) => {
      stmt.run(_d[0], _d[1], _d[2]);
    });
    stmt.finalize();
  });
}

exports.deleteDistance = (loc) => {
  db.run("DELETE FROM distance WHERE src=? OR dst=?", loc, loc);
}

exports.getDistance = (callback) => {
  db.all("SELECT * FROM distance", callback);
}

