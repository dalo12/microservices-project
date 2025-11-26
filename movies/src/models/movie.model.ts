import { Schema, model } from 'mongoose';

const movieSchema = new Schema({
  title: { type: String, required: true },
  year: { type: Number, required: true },
  genre: { type: [String], required: true },
  director: { type: String, required: true },
  actors: { type: [String], required: true },
  plot: { type: String, required: true },
  poster: { type: String, required: true },
  rating: { type: Number, required: true },
  reviews: { type: [String], required: true },
}, { collection: 'movies' });

const Movie = model('Movie', movieSchema);

export default Movie;