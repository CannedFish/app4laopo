const path = require('path');
const fs = require('fs');

const mapLocTable = require(path.join(__dirname, "./map-loc-table.js"));
const map = require(path.join(__dirname, "./map-initialize.js"));

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

function updateDis() {
  disUpdateBtn.disabled = true;
  let c_loc = [];
  let locList = mapLocTable.getLocList();
  for(let i = 0; i < locList.length; ++i) {
    c_loc.push(...locList.slice(i+1).map((_l) => {
      return [locList[i].title, _l.title];
    }));
  }
  Promise.all(c_loc.map((locSet) => {
    return map.dis_query(locSet[0], locSet[1]);
  })).then((values) => {
    disCache = values;
    disSave();
    alert("Update completed!");
    disUpdateBtn.disabled = false;
  });
}

function clearTable() {
  while(disTable.rows.length > 1) {
    disTable.deleteRow(-1);
  }
}

function addRow(re) {
  let row = disTable.insertRow();
  re.map((_r) => {
    row.insertCell().appendChild(document.createTextNode(_r));
  });
};

function search(target) {
  clearTable();
  disCache.map((dis) => {
    return [dis[0], dis[1], dis[2], Math.round(Math.abs(dis[2]-target)*10)/10];
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

