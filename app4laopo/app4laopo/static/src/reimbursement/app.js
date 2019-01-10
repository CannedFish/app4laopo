Vue.options.delimiters = ['{[{', '}]}'];

function _searchAction(evt) {
  console.log(this, tabs.targetDistance)
  tabs.results = [{
    src: {
      name_ch: '甲医院',
      lng: 0,
      address: '',
      lat: 0,
      name_en: 'Hospital Jia',
      id: '33928d120'
    },
    dst: {
      name_ch: '乙医院',
      lng: 0,
      address: '',
      lat: 0,
      name_en: 'Hospital Yi',
      id: '33928d320'
    },
    distance: '24'
  }, {
    src: {
      name_ch: '甲医院',
      lng: 0,
      address: '',
      lat: 0,
      name_en: 'Hospital Jia',
      id: '33928d120'
    },
    dst: {
      name_ch: '乙医院',
      lng: 0,
      address: '',
      lat: 0,
      name_en: 'Hospital Yi',
      id: '33928d320'
    },
    distance: '25'
  }, {
    src: {
      name_ch: '甲医院',
      lng: 0,
      address: '',
      lat: 0,
      name_en: 'Hospital Jia',
      id: '33928d120'
    },
    dst: {
      name_ch: '乙医院',
      lng: 0,
      address: '',
      lat: 0,
      name_en: 'Hospital Yi',
      id: '33928d320'
    },
    distance: '28'
  }]
}

var hospitals = []
function _getHospitals() {
  this.$http.get('/reimbursement/hospital').then(res => {
    console.log(res);
    hospitals = res.body;
    this.hospitals = hospitals;
  }, err => {
    console.log(err);
  });
}

function _addHospital(evt) {
  this.$http.get('/reimbursement/location?name=医院').then(res => {
    this.candidates = res.body;
  }, err => {
    console.log(err);
  });
}

function _handleNewHospital(idx) {
  this.$http.post('/reimbursement/hospital'
      , this.candidates[idx]).then(res => {
    this.hospitals.push(res.body);
    this.hospitalName = '';
    // NOTE: not worked
    this.$emit('input', this.hospitalName);
  }, err => {
    console.log(err);
  })
}

var idxShown = null;
var tmpDetail = null;
function _handleHospitalDetailShow(idx, evt) {
  tmpDetail = Object.assign({}, hospitals[idx]);
  tabs.hospitalDetail = hospitals[idx];
  idxShown = idx;
}

function _handleDetailSave() {
  // TODO: request to update
}

function _handleDetailCancel() {
  tabs.hospitalDetail.name_en = tmpDetail.name_en;
}

function _matchHospital(idx) {
  return !hospitals[idx].name_ch.includes(this.hospitalName)
    && !hospitals[idx].name_en.includes(this.hospitalName);
}

function _checkInput() {
  let self = this;
  this.$nextTick(() => {
    self.noMatch = (self.$el.querySelectorAll("tr.hidden").length === hospitals.length);
  });
}

var tabs = new Vue({
  el: '#nav-tabs',
  data: {
    searchTab: true,
    mgtTab: false,
    // search tab
    targetDistance: '',
    results: [],
    // mgt tab
    hospitals: [],
    hospitalName: '',
    hospitalDetail: {},
    noMatch: false,
    candidates: []
  },
  methods: {
    toggle: function (tabIdx, evt) {
      evt.preventDefault();
      evt.stopPropagation();
      this.searchTab = (tabIdx === 0);
      this.mgtTab = (tabIdx === 1);
    },
    // search tab
    searchAction: _searchAction,
    // mgt tab
    getHospitals: _getHospitals,
    addHospital: _addHospital,
    handleNewHospital: _handleNewHospital,
    handleHospitalDetailShow: _handleHospitalDetailShow,
    handleDetailSave: _handleDetailSave,
    handleDetailCancel: _handleDetailCancel,
    matchHospital: _matchHospital,
    checkInput: _checkInput
  },
  created: function () {
    _getHospitals.apply(this);
  }
});

