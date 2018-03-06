const path = require('path');
const electron = require('electron');
const BrowserWindow = electron.BrowserWindow;
const ipc = electron.ipcMain;

const debug = /--debug/.test(process.argv[2]);

let mapLocSelectWindow = null;

function instance() {
  if(mapLocSelectWindow == null) {
    const mainWin = require(path.join(__dirname, '../../main.js')).instance();
    mapLocSelectWindow = new BrowserWindow({
      width: 480,
      height: 180,
      parent: mainWin,
      modal: true,
      autoHideMenuBar: true,
      show: false,
      minimizable: false,
      maximizable: false,
      resizable: false
    });
    mapLocSelectWindow.loadURL(path.join('file://', __dirname
      , '../../sections/windows/map-loc-select.html'));
    mapLocSelectWindow.on('closed', () => {
      mapLocSelectWindow = null;
    });

    if(debug) {
      mapLocSelectWindow.webContents.openDevTools();
      require('devtron').install();
    }
  }
  return mapLocSelectWindow;
}

ipc.on('select-show', (evt, data) => {
  let win = instance();
  win.once('ready-to-show', () => {
    win.show();
  }).once('show', (evt) => {
    evt.sender.send('select-show-reply', data);
  });
}).on('loc-select', (evt, row) => {
  mapLocSelectWindow.getParentWindow().webContents.send('loc-select-reply', row);
  mapLocSelectWindow.close();
});

