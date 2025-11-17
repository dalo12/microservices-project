<template>
  <div class="home">
    <div class="banner" v-if="mainMovie">
      <img :src="mainMovie.poster" alt="Banner Poster" class="banner-img" />
      <div class="banner-info">
        <h2>{{ mainMovie.title }}</h2>
        <span>{{ mainMovie.duration }} min.</span>
        <p>{{ mainMovie.short_plot }}</p>
        <router-link :movie=mainMovie :to="`/film/${mainMovie.id}`" class="btn">
          More Info
        </router-link>
      </div>
    </div>

    <div class="movie-list">
      <h3>Recommended Films</h3>
      <div class="scroller">
        <div v-for="movie in recommended" :key="movie.id" class="movie-card">
          <router-link :to="`/movie/${movie.id}`">
            <img :src="movie.poster" :alt="movie.title" />
            <p>{{ movie.title }}</p>
          </router-link>
        </div>
      </div>
    </div>

    <div class="movie-list">
      <h3>Top Films</h3>
      <div class="scroller">
        <div v-for="movie in topFilms" :key="movie.id" class="movie-card">
          <router-link :to="`/movie/${movie.id}`">
            <img :src="movie.poster" :alt="movie.title" />
            <p>{{ movie.title }}</p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useMovieApi } from '../data/db.js';
import { api } from '@/plugins/axios.js'; 

const { getRecommended, getTop, getRandomBanner } = useMovieApi();
const mainMovie = ref({});
const topFilms = ref({});


onMounted(async () => {
  let responseMainMovie = await api.get('/random-movie');
  mainMovie.value = responseMainMovie.data || {};

  let responseTopFilms = await api.get('/top-movies/10');
  topFilms.value = responseTopFilms.data.movies || {};
})
// When the component is created, fetch the data


const recommended = ref(getRecommended());
</script>

<style scoped>
/* Add your CSS here. See basic styles in the final section. */
.banner {
  position: relative;
  background: #222;
  color: white;
  display: flex;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 2rem;
}
.banner-img {
  width: 270px;
  object-fit: cover;
}
.banner-info {
  padding: 2rem;
}
.banner-info h2 {
  margin-top: 0;
}
.btn {
  background: #42b883;
  color: white;
  padding: 10px 15px;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  display: inline-block;
  margin-top: 1rem;
}

.movie-list h3 {
  color: #222;
  font-weight: bold;
  border-bottom: 2px solid #42b883;
  padding-bottom: 5px;
  margin-bottom: 1rem;
}

.movie-list p{
  color:#222;
}
.scroller {
  display: flex;
  overflow-x: auto;
  gap: 15px;
  padding-bottom: 1rem; /* For scrollbar */
}
.movie-card {
  flex: 0 0 150px; /* Do not grow, do not shrink, base width 150px */
}
.movie-card img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  border-radius: 5px;
}
.movie-card p {
  font-size: 0.9rem;
  font-weight: bold;
  text-align: center;
  margin-top: 5px;
}
.movie-card a {
  text-decoration: none;
  color: inherit;
}
</style>