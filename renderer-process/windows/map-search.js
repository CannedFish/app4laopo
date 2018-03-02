const path = require('path');
const fs = require('fs');

const mapLocTable = require(path.join(__dirname, "./map-loc-table.js"));
const map = require(path.join(__dirname, "./map-initialize.js"));

const disFilePath = path.join(__dirname, "../../data/dis.dat");

const searchInput = document.getElementById('route-dis');
const searchBtn = document.getElementById('route-search');
const disUpdateBtn = document.getElementById('dis-update');

let disCache = null;

function updateDis() {
  mapLocTable.getLocList().map((loc) => {
  });
}

function event_init() {
  disUpdateBtn.addEventListener((evt) => {
    updateDis();
  });
}

function main() {
  event_init();
}

main();

