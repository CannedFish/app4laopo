const path = require('path');
const fs = require('fs');

const mapLocTable = require(path.join(__dirname, "./map-loc-table.js"));
const map = require(path.join(__dirname, "./map-initialize.js"));
const db = require(path.join(__dirname, "../../main-process/windows/db.js"));

const disFilePath = path.join(__dirname, "../../data/dis.dat");

const searchInput = document.getElementById('route-dis');
const searchBtn = document.getElementById('route-search');
const disUpdateBtn = document.getElementById('dis-update');
const disTable = document.getElementById('search-result-table');

let disCache = null;

function disSave() {
  fs.writeFile(disFilePath, JSON.stringify(disCache), (err) => {
    if(err) {
      console.log(err);
    }
  });
}

function disLoad() {
  fs.readFile(disFilePath, 'utf8', (err, data) => {
    if(err) {
      disCache = [];
      return ;
    }
    disCache = JSON.parse(data);
  });
}

function __promiseArray(arr, fn) {
  return arr.reduce((p, nextItem) => {
    return p.then((lastValue) => {
      return fn(nextItem, lastValue);
    });
  }, Promise.resolve([]));
}

function updateDis(locList, newLoc, callback) {
  // disUpdateBtn.disabled = true;
  // let c_loc = [];
  // let locList = mapLocTable.getLocList();
  // for(let i = 0; i < locList.length; ++i) {
    // c_loc.push(...locList.slice(i+1).map((_l) => {
      // return [locList[i], _l];
    // }));
  // }
  let c_loc = locList.map((loc) => {
    return [loc, newLoc];
  });
  let c_loc_slice = [];
  for(let i = 0; i < c_loc.length; i += 5) {
    c_loc_slice.push(c_loc.slice(i, i+5));
  }
  __promiseArray(c_loc_slice, (_c_loc, _l_values) => {
    return Promise.all(_c_loc.map((locSet) => {
      return map.dis_query(locSet[0], locSet[1]);
    })).then((values) => {
      return Promise.resolve(_l_values.concat(values));
    }).catch((reason) => {
      return Promise.resolve(_l_values.concat([9999,9999,9999,9999,9999]));
    });
  }).then((values) => {
    // disCache = values;
    // disSave();
    db.insertDistance(values);
    disCache.push(values);
    alert("Update completed!");
    // disUpdateBtn.disabled = false;
  }).catch((reason) => {
    console.log(reason);
    alert("Error happen!");
    // disUpdateBtn.disabled = false;
  });
}
exports.updateDis = updateDis;

function clearTable() {
  while(disTable.rows.length > 1) {
    disTable.deleteRow(-1);
  }
}

function addRow(re) {
  let row = disTable.insertRow();
  re.map((_r) => {
    // row.insertCell().appendChild(document.createTextNode(_r));
    row.insertCell().innerHTML = _r;
  });
};

function search(target) {
  clearTable();
  disCache.map((dis) => {
    return [dis[0], dis[1], dis[2], Math.round(Math.abs(dis[2]-target)*1000)/1000];
  }).sort((a, b) => {
    if(a[3] < b[3]) {
      return -1;
    }
    if(a[3] > b[3]) {
      return 1;
    }
    return 0;
  }).slice(0, 10).map((dis) => {
    addRow(dis);
  });
}

function eventInit() {
  disUpdateBtn.addEventListener('click', (evt) => {
    updateDis();
  });

  searchBtn.addEventListener('click', (evt) => {
    if(searchInput.value == '') {
      alert("Please input the target distance");
      return ;
    }
    search(searchInput.value);
  });
}

function main() {
  eventInit();
  disLoad();
}

main();

