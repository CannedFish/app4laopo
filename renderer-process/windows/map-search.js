const path = require('path');
const fs = require('fs');

const mapLocTable = require(path.join(__dirname, "./map-loc-table.js"));
const map = require(path.join(__dirname, "./map-initialize.js"));
const db = require(path.join(__dirname, "../../main-process/windows/db.js"));

const disFilePath = path.join(__dirname, "../../data/dis.dat");

const searchInput = document.getElementById('route-dis');
const searchBtn = document.getElementById('route-search');
// const disUpdateBtn = document.getElementById('dis-update');
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
  // fs.readFile(disFilePath, 'utf8', (err, data) => {
    // if(err) {
      // disCache = [];
      // return ;
    // }
    // disCache = JSON.parse(data);
  // });
  db.getDistance((err, rows) => {
    disCache = rows.map((row) => {
      return [row.src, row.dst, row.dis];
    });
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
    Array.prototype.push.apply(disCache, values);
    alert("Update completed!");
    callback(null);
    // disUpdateBtn.disabled = false;
  }).catch((reason) => {
    console.log(reason);
    alert("Error happen!");
    // disUpdateBtn.disabled = false;
    callback(reason);
  });
}
exports.updateDis = updateDis;

exports.removeDis = (loc) => {
  let _loc = typeof(loc.enTitle) === 'undefined' ? loc.title : `${loc.title}<br>${loc.enTitle}`;
  db.deleteDistance(_loc);
  disLoad();
}

exports.updateDisTitle = (loc, oldEnTitle) => {
  let newTilte = `${loc.title}<br>${loc.enTitle}`;
  let oldTitle = typeof(oldEnTitle) === 'undefined' ? loc.title : `${loc.title}<br>${oldEnTitle}`;
  db.updateDistanceTitle(oldTitle, newTilte);
  disLoad();
}

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

function __searchFilter() {
  if(endpointInput.value != "") {
    return disCache.filter((dis) => {
      return dis[0].includes(endpointInput.value) || dis[1].includes(endpointInput.value);
    });
  }
  return disCache;
}

function search(target) {
  clearTable();
  let candidate = null;
  __searchFilter(disCache).map((dis) => {
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

function __search() {
  if(searchInput.value == '') {
    alert("Please input the target distance");
    return ;
  }
  search(searchInput.value);
}

// End points options
const endpointInput = document.querySelector('#endpoint');
const endDropDown = document.querySelector('#end-drop-down');
const endSelectOption = document.querySelector('#end-option');
let endOptions = [];

function showOption(options) {
  endSelectOption.innerHTML = options.map((opt) => {
    return `<li>${opt}</li>`;
  }).join('');
  endSelectOption.querySelectorAll("li").forEach((e) => {
    e.addEventListener('mouseover', (evt) => {
      evt.stopPropagation();
      endpointInput.value = evt.target.innerHTML;
    });
  });
}

function optionInit() {
  endOptions = require(path.join(__dirname, "./map-loc-table.js")).getLocList().map((loc) => {
    return loc.title;
  });
}

// events
function eventInit() {
  // disUpdateBtn.addEventListener('click', (evt) => {
    // updateDis();
  // });

  searchBtn.addEventListener('click', (evt) => {
    __search();
  });

  searchInput.addEventListener('keypress', (evt) => {
    if(evt.key == 'Enter') {
      __search();
    }
  });

  // End point select
  endpointInput.addEventListener('focus', (evt) => {
    endDropDown.classList.remove("is-hidden");
    optionInit();
    showOption(endOptions);
  });
  endpointInput.addEventListener('blur', (evt) => {
    endDropDown.classList.add("is-hidden");
  });
  endpointInput.addEventListener('input', (evt) => {
    evt.stopPropagation();
    if(endpointInput.value == '') {
      showOption(endOptions);
    } else {
      showOption(endOptions.filter((opt) => {
        return opt.includes(endpointInput.value);
      }));
    }
  });
}

function main() {
  eventInit();
  disLoad();
}

main();

