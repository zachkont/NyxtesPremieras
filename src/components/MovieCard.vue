<template>
  <v-flex>
    <v-card
      class="mx-auto"
      max-width="344"
      :color="movie.selected ? 'primary' : 'white'"
      v-on:click="clickHandler(movie)"
    >
      <v-card-text>
        <div>{{movie.room}}</div>
        <v-list-item-title class="subtitle-2 mb-1">{{movie.subtitle}}</v-list-item-title>
        <p class="display-1 text--primary">{{movie.title}}</p>
        <p>{{movie.category}}</p>
        <div class="text--primary">{{movie.description}}</div>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="deep-purple accent-4">Learn More</v-btn>
      </v-card-actions>
    </v-card>
  </v-flex>
</template>

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