const path = require('path');
const settings = require('electron-settings');
const prompt = require('electron-prompt');

const mapLocTable = require(path.join(__dirname, "./map-loc-table.js"));

const locInput = document.getElementById('map-loc');
const searchAddBtn = document.getElementById('map-search-add');
const searchBtn = document.getElementById('map-search');

function mapSearch(map, callback) {
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

exports.evt_init = (map) => {
  searchAddBtn.addEventListener('click', (e) => {
    mapSearch(map, (rs) => {
      for(let i = 0; i < rs.getCurrentNumPois(); i++) {
        mapLocTable.addRow(rs.getPoi(i));
      }
    });
  });

  searchBtn.addEventListener('click', (e) => {
    mapSearch(map, (rs) => {
      let s = [];
      for(let i = 0; i < rs.getCurrentNumPois(); i++) {
        s.push(`${rs.getPoi(i).title}, ${rs.getPoi(i).address}`);
        console.log(rs.getPoi(i));
      }
      alert(s.join('\n'));
    });
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

