const path = require('path');
const fs = require('fs');
const ipc = require('electron').ipcRenderer;

const locTable = document.getElementById('loc-table');

const dataPath = path.join(__dirname, "../../data");
const locFilePath = path.join(__dirname, "../../data/loc.dat");
// const mapSearch = require(path.join(__dirname, "./map-search.js"));

let locCache = null;

exports.getLocList = () => {
  return locCache;
}

exports.getLocByTitle = (locTitle) => {
  return locCache.find((e) => {
    return e.title == locTitle;
  });
}

function locCacheSave() {
  fs.writeFile(locFilePath, JSON.stringify(locCache), (err) => {
    if(err) {
      console.log(err);
    }
  });
}
exports.save = locCacheSave;

function locCacheLoad() {
  fs.readFile(locFilePath, 'utf8', (err, data) => {
    if(err) {
      locCache = [];
      return ;
    }
    // restore loc to loc table
    locCache = JSON.parse(data);
    locCache.map(addRow);
    locCache.splice(locCache.length/2);
    console.log(locCache);
  });
}

function addRow(loc) {
  let row = locTable.insertRow();
  row.insertCell().appendChild(document.createTextNode(loc.title));
  row.insertCell().appendChild(document
    .createTextNode(typeof(loc.enTitle) === 'undefined' ? '' : loc.enTitle));
  row.insertCell().appendChild(document.createTextNode(loc.address));
  
  let actionCell = row.insertCell();
  let editBtn = document.createElement('button');
  editBtn.innerHTML = "edit";
  editBtn.addEventListener('click', (e) => {
    ipc.send('edit-show', loc, row.rowIndex, locCache.indexOf(loc));
  });
  actionCell.appendChild(editBtn);
  let deleteBtn = document.createElement('button');
  deleteBtn.innerHTML = "delete";
  deleteBtn.addEventListener('click', (e) => {
    // TODO: need a confirm
    // update distance database
    require(path.join(__dirname, "./map-search.js")).removeDis(loc);
    locTable.deleteRow(row.rowIndex);
    locCache.splice(locCache.indexOf(loc), 1);
    // console.log(locCache);
    locCacheSave();
  });
  actionCell.appendChild(deleteBtn);

  locCache.push(loc);
  // console.log(locCache);
}; 
exports.addRow = addRow;

ipc.on('loc-select-reply', (evt, row) => {
  // update distance
  const mapSearch = require(path.join(__dirname, "./map-search.js"));
  mapSearch.updateDis(locCache, row, (err) => {
    if(err) {
      return ;
    }
    addRow(row);
    locCacheSave();
  });
}).on('edit-confirm-reply', (evt, loc, tableIdx, cacheIdx) => {
  locCache[cacheIdx].enTitle = loc.enTitle;
  locCacheSave();

  let row = locTable.rows[tableIdx];
  row.deleteCell(1);
  row.insertCell(1).appendChild(document.createTextNode(loc.enTitle));
});

exports.init = () => {
  if(!fs.existsSync(dataPath)) {
    fs.mkdirSync(dataPath);
  }

  locCacheLoad();
};

