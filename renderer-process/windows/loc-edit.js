const ipc = require('electron').ipcRenderer;

const infoTable = document.getElementById("loc-info");
const infoConfirmBtn = document.getElementById("info-confirm");
const infoCancelBtn = document.getElementById("info-cancel");

function tableInit(loc) {
  let titleRow = infoTable.insertRow();
  titleRow.insertCell().appendChild(document.createTextNode('Name'));
  titleRow.insertCell().appendChild(document.createTextNode(loc.title));

  let enTitleRow = infoTable.insertRow();
  enTitleRow.insertCell().appendChild(document.createTextNode('Name(EN)'));
  let enTitleInput = document.createElement('input');
  enTitleInput.placeholder = "English name of this location";
  enTitleInput.style.width = '100%';
  enTitleRow.insertCell().appendChild(enTitleInput);
  if(typeof(loc.enTitle) !== 'undefined') {
    enTitleInput.value = loc.enTitle;
  }

  let addressRow = infoTable.insertRow();
  addressRow.insertCell().appendChild(document.createTextNode('Address'));
  addressRow.insertCell().appendChild(document.createTextNode(loc.address));

  infoConfirmBtn.addEventListener('click', (evt) => {
    loc.enTitle = enTitleInput.value;
    ipc.send('edit-confirm', loc);
  });
  infoCancelBtn.addEventListener('click', (evt) => {
    ipc.send('edit-cancel');
  });
}

ipc.on('edit-show-reply', (evt, locData) => {
  tableInit(locData);
});

