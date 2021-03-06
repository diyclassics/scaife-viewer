import Vue from 'vue';
import VueRouter from 'vue-router';
import { sync } from 'vuex-router-sync';
import vueCustomElement from 'vue-custom-element';
import CTSTextGroupList from './components/CTSTextGroupList';
import CTSWorkList from './components/CTSWorkList';
import CTSTocList from './components/CTSTocList';
import router from './router';
import store from './store';

sync(store, router);

Vue.use(VueRouter);
Vue.use(vueCustomElement);

Vue.customElement('sv-cts-textgroup-list', CTSTextGroupList);
Vue.customElement('sv-cts-work-list', CTSWorkList);
Vue.customElement('sv-cts-toc-list', CTSTocList);
Vue.customElement('sv-reader', {
  router, // tied to sv-reader until we vueify the whole site
  template: '<router-view />',
});
