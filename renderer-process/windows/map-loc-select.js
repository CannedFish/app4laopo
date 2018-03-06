const ipc = require('electron').ipcRenderer;

const selectTable = document.getElementById('selection');

let dataCache = null;

ipc.on('select-show-reply', (evt, data) => {
  dataCache = data;
  data.map((_d) => {
    let row = selectTable.insertRow();
    row.insertCell().appendChild(document.createTextNode(_d.title));
    row.insertCell().appendChild(document.createTextNode(_d.address));

    row.addEventListener('click', (evt) => {
      ipc.send('loc-select', dataCache[row.rowIndex]);
    });
  });
});

