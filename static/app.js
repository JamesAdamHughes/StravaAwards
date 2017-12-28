Vue.use(VueMaterial.default)

var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello James',
    awards : []
  },
  created: function(){
    this.$http.get('/api/award/list/14906240?onlyNew=false&email=false').then((response) => {
      console.log(response)
      this.awards = response.data.awards;
    });
  }
})
// Vue.component('award-tile', {
//   props: ['name', 'icon', 'lastAwarded', 'text']
//   // templa
// })