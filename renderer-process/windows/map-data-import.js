const ipc = require('electron').ipcRenderer;
const {dialog} = require('electron').remote;

const confirmBtn = document.querySelector("#import-confirm");
const cancelBtn = document.querySelector("#import-cancel");
const locDataInput = document.querySelector("#loc-data");
const locDataBtn = document.querySelector("#loc-data-btn");
const disDataInput = document.querySelector("#dis-data");
const disDataBtn = document.querySelector("#dis-data-btn");

confirmBtn.addEventListener('click', (evt) => {
  if(locDataInput.value == '' && disDataInput.value == '') {
    return alert("Please at least assign one data source.");
  }
  ipc.send('data-import-confirm', locDataInput.value, disDataInput.value);
});

cancelBtn.addEventListener('click', (evt) => {
  ipc.send('data-import-cancel');
});

locDataBtn.addEventListener('click', (evt) => {
  dialog.showOpenDialog({
    properties: ["openFile"] 
  }, (src) => {
    locDataInput.value = src[0];
    locDataInput.title = src[0];
  });
});

disDataBtn.addEventListener('click', (evt) => {
  dialog.showOpenDialog({
    properties: ["openFile"] 
  }, (src) => {
    disDataInput.value = src[0];
    disDataInput.title = src[0];
  });
});

