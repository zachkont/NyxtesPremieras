<template>
  <v-flex>
    <v-card
      class="mx-auto"
      max-width="300"
      :color="movie.selected ? 'primary' : 'white'"
      v-on:click="clickHandler(movie)"
    >
      <v-card-text>
        <div>{{movie.room}}</div>
        <p class="np-time">{{movie.time}}</p>
        <v-list-item-title class="subtitle-2 mb-1">{{movie.subtitle}}</v-list-item-title>
        <p class="np-title text--primary">{{movie.title}}</p>
        <p>{{movie.category}}</p>
        <div class="np-description text--primary">{{movie.description}}</div>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="deep-purple accent-4">Learn More</v-btn>
      </v-card-actions>
    </v-card>
  </v-flex>
</template>

<style scoped>
  .np-title {
    font-size: 18px;
    font-weight: 700;
    line-height: 1.5rem;
    letter-spacing: 0.0073529412em !important;
    font-family: "Roboto", sans-serif !important;
  }

  .np-description {
    font-size: 16px;
    font-weight: 400;
  }
  
  .np-time {
    font-weight: 700;
  }
</style>

<script>
import { mapActions } from "vuex";

export default {
  props: ["movie"],
  data: () => ({}),
  methods: {
    ...mapActions({
      clickHandler: "clickMovie"
    })
  }
};
</script>