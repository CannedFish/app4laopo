Vue.options.delimiters = ['{[{', '}]}'];

var tabs = new Vue({
  el: '#nav-tabs',
  data: {
    searchTab: true,
    mgtTab: false,
    targetDistance: '',
    results: []
  },
  methods: {
    toggle: (tabIdx, evt) => {
      evt.preventDefault();
      evt.stopPropagation();
      tabs.searchTab = (tabIdx === 0);
      tabs.mgtTab = (tabIdx === 1);
    },
    searchAction: (evt) => {
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
  }
});

