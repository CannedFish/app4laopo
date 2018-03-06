const path = require('path');
const electron = require('electron');
const BrowserWindow = electron.BrowserWindow;
const ipc = electron.ipcMain;

const debug = /--debug/.test(process.argv[2]);

let locEditWindow = null;

function instance() {
  if(locEditWindow == null) {
    const mainWin = require(path.join(__dirname, '../../main.js')).instance();
    locEditWindow = new BrowserWindow({
      width: 480,
      height: 200,
      parent: mainWin,
      modal: true,
      autoHideMenuBar: true,
      show: false,
      // resizable: false,
      minimizable: false,
      maximizable: false
    });
    locEditWindow.loadURL(path.join('file://', __dirname
      , '../../sections/windows/loc-edit.html'));
    locEditWindow.on('closed', () => {
      locEditWindow = null;
    });

    if(debug) {
      locEditWindow.webContents.openDevTools();
      require('devtron').install();
    }
  }
  return locEditWindow;
}

let _tableIdx = null;
let _cacheIdx = null;

ipc.on('edit-show', (evt, locData, tableIdx, cacheIdx) => {
  let win = instance();
  _tableIdx = tableIdx;
  _cacheIdx = cacheIdx;
  win.once('ready-to-show', () => {
    win.show();
  }).once('show', (evt) => {
    evt.sender.send('edit-show-reply', locData);
  });
}).on('edit-confirm', (evt, loc) => {
  locEditWindow.getParentWindow().webContents.send('edit-confirm-reply'
    , loc, _tableIdx, _cacheIdx);
  locEditWindow.close();
}).on('edit-cancel', (evt) => {
  locEditWindow.close()
});

