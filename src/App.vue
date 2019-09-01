<template>
  <v-app>
    <Toolbar></Toolbar>
    <v-content id="content">
      <v-container fluid>
        <Grid />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Grid from "./components/Grid";
import Toolbar from "./components/Toolbar";

export default {
  name: "App",
  components: {
    Grid,
    Toolbar
  },
  data: () => ({}),
};
</script>