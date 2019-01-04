Vue.options.delimiters = ['{[{', '}]}'];

function _searchAction(evt) {
  console.log(tabs.targetDistance)
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
  hospitals = [{
    name_ch: '甲医院',
    lng: 0,
    address: '甲路1号',
    lat: 0,
    name_en: 'Hospital Jia',
    id: '33928d323'
  }, {
    name_ch: '乙医院',
    lng: 0,
    address: '乙路1号',
    lat: 0,
    name_en: 'Hospital Yi',
    id: '33928d320'
  }, {
    name_ch: '丙医院',
    lng: 0,
    address: '丙路1号',
    lat: 0,
    name_en: 'Hospital Bing',
    id: '33958d320'
  }, {
    name_ch: '丁医院',
    lng: 0,
    address: '丁路1号',
    lat: 0,
    name_en: 'Hospital Ding',
    id: '33998d320'
  }];
  return hospitals;
}

function _searchHospital(evt) {
}

function _handleHospitalDetailShow(idx, evt) {
  console.log(idx, evt.relatedTarget);
  tabs.hospitalDetail = hospitals[idx];
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
    hospitalName: '',
    hospitalDetail: {}
  },
  methods: {
    toggle: (tabIdx, evt) => {
      evt.preventDefault();
      evt.stopPropagation();
      tabs.searchTab = (tabIdx === 0);
      tabs.mgtTab = (tabIdx === 1);
    },
    // search tab
    searchAction: _searchAction,
    // mgt tab
    getHospitals: _getHospitals,
    searchHospital: _searchHospital,
    handleHospitalDetailShow: _handleHospitalDetailShow
  }
});

