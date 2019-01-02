Vue.options.delimiters = ['{[{', '}]}'];

var tabs = new Vue({
  el: '#nav-tabs',
  data: {
    searchTab: true,
    mgtTab: false
  },
  methods: {
    toggle: (tabIdx, evt) => {
      evt.preventDefault();
      evt.stopPropagation();
      tabs.searchTab = (tabIdx === 0);
      tabs.mgtTab = (tabIdx === 1);
    }
  }
});

