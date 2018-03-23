const path = require('path');
const electron = require('electron');
const BrowserWindow = electron.BrowserWindow;
const ipc = electron.ipcMain;

const debug = /--debug/.test(process.argv[2]);

let dataImportWindow = null;

function instance() {
  if(dataImportWindow == null) {
    const mainWin = require(path.join(__dirname, '../../main.js')).instance();
    dataImportWindow = new BrowserWindow({
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
    dataImportWindow.loadURL(path.join('file://', __dirname
      , '../../sections/windows/map-data-import.html'));
    dataImportWindow.on('closed', () => {
      dataImportWindow = null;
    });

    if(debug) {
      dataImportWindow.webContents.openDevTools();
      require('devtron').install();
    }
  }
  return dataImportWindow;
}

let _tableIdx = null;
let _cacheIdx = null;

ipc.on('data-import-show', (evt) => {
  let win = instance();
  win.once('ready-to-show', () => {
    win.show();
  }).once('show', (evt) => {
    evt.sender.send('import-show-reply');
  });
}).on('data-import-confirm', (evt, locData, disData) => {
  dataImportWindow.getParentWindow().webContents.send('data-import-confirm-reply'
    , locData, disData);
  dataImportWindow.close();
}).on('data-import-cancel', (evt) => {
  dataImportWindow.close();
});

