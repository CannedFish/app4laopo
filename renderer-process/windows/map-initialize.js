const path = require('path');
const settings = require('electron-settings');
const prompt = require('electron-prompt');
const ipc = require('electron').ipcRenderer;

const mapLocTable = require(path.join(__dirname, "./map-loc-table.js"));

const locInput = document.getElementById('map-loc');
// const searchAddBtn = document.getElementById('map-search-add');
const searchBtn = document.getElementById('map-search');

let map = null;

function mapSearch(callback) {
  if(locInput.value == '') {
    alert("Please input a localtion name.");
  } else {
    let options = {
      onSearchComplete: (rs) => {
        if(local.getStatus() == BMAP_STATUS_SUCCESS) {
          callback(rs);
        }
      }
    };
    let local = new BMap.LocalSearch(map, options);
    local.search(locInput.value);
  }
}

function searchLoc() {
  searchBtn.disabled = true;
  mapSearch((rs) => {
    let data = [];
    for(let i = 0; i < rs.getCurrentNumPois(); i++) {
      data.push(rs.getPoi(i));
    }
    ipc.send('select-show', data);
    searchBtn.disabled = false;
  });
}

exports.evt_init = () => {
  /* searchAddBtn.addEventListener('click', (e) => { */
    // mapSearch((rs) => {
      // for(let i = 0; i < rs.getCurrentNumPois(); i++) {
        // mapLocTable.addRow(rs.getPoi(i));
      // }
      // mapLocTable.save();
    // });
  /* }); */

  searchBtn.addEventListener('click', (e) => {
    searchLoc();
  });

  locInput.addEventListener('keypress', (evt) => {
    if(evt.key == "Enter") {
      searchLoc();
    }
  });
};

exports.map_init = (_map) => {
  map = _map;
};

const re = /[\d.]+/;
exports.dis_query = (src, dst) => {
  return new Promise((resolve, reject) => {
    try {
      let transit = new BMap.DrivingRoute(map, {
        onSearchComplete: (rs) => {
          resolve([
            typeof(src.enTitle) === 'undefined' ? src.title : `${src.title}<br>${src.enTitle}`,
            typeof(dst.enTitle) === 'undefined' ? dst.title : `${dst.title}<br>${dst.enTitle}`, 
            // Number(re.exec(rs.getPlan(0).getDistance(true))[0])
            rs.taxiFare == null ? 0 : rs.taxiFare.distance / 1000
          ]);
        }
      });
      transit.search(src, dst);
    } catch(e) {
      reject(e);
    }
  });
};

function main() {
  let ak = settings.get('map-ak');
  let script = document.createElement("script");
  if(ak == null) {
    prompt({
      title: 'Map key',
      label: 'Please input the map key'
    }).then((r) => {
      if(r == null) {
        throw "Map key is not given"
      }
      settings.set('map-ak', r)
      script.src = `http://api.map.baidu.com/api?v=2.0&ak=${r}&callback=initialize`;
      document.body.appendChild(script);
    }).catch((e) => {
      console.error(e)
      throw "We need map key!!"
    });
  } else {
    script.src = `http://api.map.baidu.com/api?v=2.0&ak=${ak}&callback=initialize`;
    document.body.appendChild(script);
  }

  mapLocTable.init();
}

main();

