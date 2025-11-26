const mongoose = require('mongoose');

const imdbSchema = new mongoose.Schema({
  rating: Number,
  votes: Number,
  id: Number
});

const tomatoRatingSchema = new mongoose.Schema({
  rating: Number,
  numReviews: Number,
  meter: Number
});

const tomatoesSchema = new mongoose.Schema({
  viewer: tomatoRatingSchema,
  critic: tomatoRatingSchema,
  lastUpdated: String
});

const awardsSchema = new mongoose.Schema({
  wins: Number,
  nominations: Number,
  text: String
});

const filmSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  year: {
    type: Number,
    required: true
  },
  runtime: Number,
  released: String,
  plot: String,
  fullplot: String,
  type: String,
  directors: [String],
  cast: [String],
  countries: [String],
  genres: [String],
  imdb: imdbSchema,
  tomatoes: tomatoesSchema,
  awards: awardsSchema
}, {
  timestamps: true
});

// Create indexes for better performance
filmSchema.index({ title: 'text', plot: 'text' });
filmSchema.index({ year: 1 });
filmSchema.index({ genres: 1 });
filmSchema.index({ 'imdb.rating': -1 });

module.exports = mongoose.model('Film', filmSchema, 'movies');