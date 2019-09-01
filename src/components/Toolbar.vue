<template v-slot:img="{ props }">
  <v-app-bar
    app
    :color="anyMovieIsSelected ? '#2A2A84' : '#711B5A'"
    dark
    fixed
    shrink-on-scroll
    fade-img-on-scroll
    src="http://media.interactive.netuse.gr/filesystem/images/20190827/engine/24-aiff-cover_981_14350080_type14003.jpg"
  >
    <template v-slot:img="{ props }">
      <v-img v-bind="props" gradient="to top right, rgba(252,5,42,.6), rgba(34,34,101,.8)"></v-img>
    </template>

    <!-- <v-app-bar-nav-icon></v-app-bar-nav-icon> -->

    <v-toolbar-title>Νύχτες Πρεμιέρας</v-toolbar-title>
    <div class="flex-grow-1"></div>

    <!-- Clear selected -->
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn icon v-if="anyMovieIsSelected" @click="clearSelectedMovies" v-on="on">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
      <span>Καθαρισμός επιλογών</span>
    </v-tooltip>

    <!-- Clear filter / Show all movies -->
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn icon v-if="filterActive" @click="toggleFilter" v-on="on">
          <v-icon>mdi-filter-remove-outline</v-icon>
        </v-btn>
      </template>
      <span>Εμφάνιση όλων</span>
    </v-tooltip>

    <!-- Filter movies -->
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn icon v-if="anyMovieIsSelected && !filterActive" @click="toggleFilter" v-on="on">
          <v-icon>mdi-filter-outline</v-icon>
        </v-btn>
      </template>
      <span>Αποκρυψη μη επιλεγμένων</span>
    </v-tooltip>

  </v-app-bar>
</template>

<script>
import { mapActions, mapState, mapGetters } from "vuex";

export default {
  data: () => ({}),
  computed: {
    ...mapState(["filterActive"]),
    ...mapGetters(["anyMovieIsSelected"])
  },
  methods: {
    ...mapActions(["toggleFilter", "clearSelectedMovies"])
  }
};
</script>