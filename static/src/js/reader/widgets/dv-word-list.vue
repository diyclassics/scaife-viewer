<template>
  <widget class="word-list" v-if="show">
    <span slot="header">Word List</span>
    <div slot="body">
      <p class="legend">Number in parentheses is frequency per 10k in this work.</p>
      <p v-for="word in wordList" :key="word.text">
        <span class="w">{{ word.text }}</span>
        <span class="df">{{ word.shortdef }}</span>
        <span class="fr">({{ word.frequency }})</span>
      </p>
    </div>
  </widget>
</template>

<script>
import store from '../../store';
import widget from '../widget';

export default {
  store,
  computed: {
    passage() {
      return this.$store.getters['reader/passage'];
    },
  },
  data() {
    return {
      show: false,
      wordList: [],
    };
  },
  mounted() {
    this.fetchWordList();
  },
  watch: {
    passage: 'fetchWordList',
  },
  methods: {
    async fetchWordList() {
      const server = 'https://gu658.us1.eldarioncloud.com';
      const { urn } = this.passage;
      const res = await fetch(`${server}/word-list/${urn}/json/?page=all&amp;o=1`);
      if (!res.ok) {
        if (res.status === 404) {
          this.show = false;
          return;
        }
        throw new Error(res.status);
      }
      if (this.show === false) {
        this.show = true;
      }
      const data = await res.json();
      this.wordList = data.lemmas.map(lemma => ({
        text: lemma.lemma_text,
        shortdef: lemma.shortdef,
        frequency: lemma.work_frequency.toFixed(2),
      }));
    },
  },
  components: {
    widget,
  },
};
</script>
