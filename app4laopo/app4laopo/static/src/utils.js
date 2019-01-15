Vue.options.delimiters = ['{[{', '}]}'];

let alerts = new Vue({
  el: '#alerts',
  data: {
    msgs: []
  },
  methods: {
    add: function (msg) {
      /* msg: Object, {
       *   timeout: ms to show,
       *   info: info to show,
       *   level: message's level to show, success|warning|danger
       * }
       * */
      this.msgs.push(msg);
      let self = this;
      setTimeout(() => {
        self.msgs.splice(self.msgs.indexOf(msg), 1);
      }, msg.timeout);
    }
  }
});

