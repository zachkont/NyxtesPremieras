import Vue from 'vue';
import Vuex from 'vuex';
import VuexPersistence from 'vuex-persist';
import movies from './movieList';
import _ from 'lodash';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    movies,
    filteredMovies: [],
    filterActive: false
  },
  getters: {
    displayedMovies(state) {
      let dm = [];
      if (state.filterActive) {
        dm = state.filteredMovies;
      } else {
        dm = state.movies;
      }
      return dm.reduce((acc, movie) => {
        const timestamp = new Date(movie.datetime);
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const day = timestamp.toLocaleDateString('el-GR', options);
        if (!acc[day]) {
          acc[day] = [movie];
        } else {
          acc[day].push(movie);
        }
        return acc;
      }, {});
    },
    anyMovieIsSelected(state) {
      return state.movies.reduce((acc, curr) => acc || curr.selected, false);
    }
  },
  mutations: {
    selectMovie(state, movie) {
      let a = 1;
      if (a === 1) {
        state.movies.push('test');
      }
      state.movies.pop();
      const index = _.findIndex(state.movies, movie);
      state.movies[index].selected = true;
    },
    deselectMovie(state, movie) {
      const index = _.findIndex(state.movies, movie);
      state.movies[index].selected = false;
    },
    toggleMovie(state, movie) {
      const index = _.findIndex(state.movies, movie);
      state.movies[index].selected = !state.movies[index].selected;
    },
    toggleFilter(state) {
      state.filterActive = !state.filterActive;
    },
    updateFilteredMovies(state) {
      if (state.filterActive) {
        state.filteredMovies = state.movies.filter(movie => {
          return movie.selected;
        });
        _.forEach(state.movies, (movie) => { movie.selected = false; })
      } else {
        _.forEach(state.movies, (movie) => {
          if (_.find(state.filteredMovies, movie)) {
            movie.selected = true;
          } else {
            movie.selected = false;
          }
        })
        state.filteredMovies = []
      }
    },
    clearSelectedMovies(state) {
      _.forEach(state.movies, (movie) => {
        movie.selected = false;
      })
    }
  },
  actions: {
    clickMovie(context, movie) {
      if (context.state.filterActive) {
        return;
      }
      if (movie.selected) {
        context.commit('deselectMovie', movie);
      } else {
        context.commit('selectMovie', movie);
      }
    },
    toggleFilter(context) {
      context.commit('toggleFilter');
      context.commit('updateFilteredMovies');
    },
    clearSelectedMovies(context) {
      context.commit('clearSelectedMovies');
    }
  },
  plugins: [new VuexPersistence().plugin]
})
