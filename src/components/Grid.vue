<template>
  <v-container grid-list-md text-xs-center>
    <v-layout v-for="(movies, day) in displayedMovies" v-bind:key="day" row wrap>
      <div class="divider display-1">
        {{day}}
      <v-divider></v-divider>
      </div>
      <MovieCard
        v-for="movie in movies"
        v-bind:key="movie.id"
        v-bind:movie="movie"
      ></MovieCard>
    </v-layout>
  </v-container>
</template>

<style scoped>
  .divider {
    flex: 1 1 100%;
    color: rgba(0, 0, 0, 0.54);
    text-align: center;
    margin: 20px;
  }
</style>

<script>
import MovieCard from "./MovieCard";
import { mapState, mapGetters } from 'vuex'

export default {
  components: {
    MovieCard
  },
  data: () => ({}),
    computed: {
    ...mapState([
      'filterActive',
    ]),
    ...mapGetters([
      'displayedMovies',
    ]),
  }
};
</script>