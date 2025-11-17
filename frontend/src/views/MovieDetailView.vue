<template>
  <p>{{ JSON.stringify(movie) }}</p>
  <div class="movie-detail" v-if="movie">
    <div class="detail-banner" :style="{ backgroundImage: `url(${movie.poster})` }">
      <h1>{{ movie.title }}</h1>
    </div>

    <div class="detail-content">
      <div class="poster-col">
        <img :src="movie.poster" :alt="movie.title" class="poster-img" />
      </div>
      <div class="info-col">
        <h2>{{ movie.title }}</h2>
        <span class="meta">{{ movie.duration }} | Directed by: {{ movie.director }}</span>

        <h3>Plot</h3>
        <p>{{ movie.plot_long }}</p>

        <h3>Main Cast</h3>
        <ul>
          <li v-for="actor in movie.cast" :key="actor">{{ actor }}</li>
        </ul>

        <h3>Rate this Film</h3>
        <div class="rating">
          <span
            v-for="star in 5"
            :key="star"
            @click="setRating(star)"
            class="star"
            :class="{ rated: star <= currentRating }"
          >
            ★
          </span>
        </div>
        <p v-if="currentRating > 0">Your rating: {{ currentRating }} out of 5</p>
      </div>
    </div>
  </div>
  <div v-else>
    <p>Loading movie...</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useMovieApi } from '../data/db.js';
import { api } from '@/plugins/axios.js';

/* const props = defineProps({
  movie: {
    type: Object,
    required: true,
  }
}); */

// Get the 'id' prop from the router
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const { getMovieById } = useMovieApi();

// Fetch the movie data using the id
const movie = ref({});
//const movie = ref(getMovieById(props.id));

// Local state for rating
const currentRating = ref(movie.value ? movie.value.rating : 0);

const setRating = (star) => {
  currentRating.value = star;
  // In a real app, you would also post this to your API
  // e.g., api.post(`/movies/${props.id}/rate`, { rating: star })
};

onMounted( async  () => {
  let responseMovie = await api.get(`/movie/${props.id}`);
  movie.value = responseMovie.data;
})
</script>

<style scoped>
.detail-banner {
  height: 300px;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: flex-end;
  padding: 2rem;
  color: white;
  border-radius: 8px;
  position: relative;
}
/* Scrim/overlay for text readability */
.detail-banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(0deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 50%);
  border-radius: 8px;
}
.detail-banner h1 {
  position: relative; /* Bring text above overlay */
  margin: 0;
  font-size: 3rem;
  text-shadow: 2px 2px 4px #000;
}

.detail-content {
  display: flex;
  margin-top: 2rem;
  gap: 2rem;
}
.poster-col {
  flex: 0 0 250px;
}
.poster-img {
  width: 100%;
  border-radius: 5px;
}
.info-col {
  flex: 1;
}
.meta {
  font-style: italic;
  color: #555;
  display: block;
  margin-bottom: 1.5rem;
}

.rating .star {
  font-size: 2rem;
  color: #ccc;
  cursor: pointer;
}
.rating .star.rated {
  color: #f39c12;
}
</style>