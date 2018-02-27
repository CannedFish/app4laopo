const path = require('path');
const fs = require('fs');

const locTable = document.getElementById('loc-table');

const dataPath = path.join(__dirname, "../../data");
const locFilePath = path.join(__dirname, "../../data/loc.dat");
// const disFilePath = path.join(__dirname, "../../data/dis.dat");

let locCache = null;
// TODO: locCache persistance

exports.addRow = (loc) => {
  let row = locTable.insertRow();
  row.insertCell().appendChild(document.createTextNode(loc.title));
  row.insertCell().appendChild(document.createTextNode(loc.address));

  let actionCell = row.insertCell();
  let deleteBtn = document.createElement('button');
  deleteBtn.innerHTML = "delete";
  deleteBtn.addEventListener('click', (e) => {
    locTable.deleteRow(row.rowIndex);
    locCache.splice(locCache.indexOf(loc), 1);
    console.log(locCache);
  });
  actionCell.appendChild(deleteBtn);

  locCache.push(loc);
  console.log(locCache);
};

exports.init = () => {
  if(!fs.existsSync(dataPath)) {
    fs.mkdirSync(dataPath);
  }
  
  fs.readFile(locFilePath, 'utf8', (err, data) => {
    if(err.code == "ENOENT") {
      locCache = [];
      return ;
    }
    // TODO: restore loc to loc table
  });
};

