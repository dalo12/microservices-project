const Film = require('../models/Film');

const resolvers = {
  Query: {
    films: async (_, { limit = 10, skip = 0, filter = {} }) => {
      try {
        let query = {};
        
        // Build query based on filters
        if (filter.title) {
          query.title = { $regex: filter.title, $options: 'i' };
        }
        if (filter.year) {
          query.year = filter.year;
        }
        if (filter.genre) {
          query.genres = { $in: [filter.genre] };
        }
        if (filter.director) {
          query.directors = { $in: [new RegExp(filter.director, 'i')] };
        }
        if (filter.cast) {
          query.cast = { $in: [new RegExp(filter.cast, 'i')] };
        }

        return await Film.find(query)
          .limit(limit)
          .skip(skip)
          .sort({ year: -1 });
      } catch (error) {
        throw new Error('Error fetching films: ' + error.message);
      }
    },

    film: async (_, { id }) => {
      try {
        const film = await Film.findById(id);
        if (!film) {
          throw new Error('Film not found');
        }
        return film;
      } catch (error) {
        throw new Error('Error fetching film: ' + error.message);
      }
    },

    searchFilms: async (_, { title }) => {
      try {
        return await Film.find({
          title: { $regex: title, $options: 'i' }
        }).limit(20);
      } catch (error) {
        throw new Error('Error searching films: ' + error.message);
      }
    },

    filmsByGenre: async (_, { genre }) => {
      try {
        return await Film.find({
          genres: { $in: [genre] }
        }).limit(20).sort({ 'imdb.rating': -1 });
      } catch (error) {
        throw new Error('Error fetching films by genre: ' + error.message);
      }
    },

    filmsByYearRange: async (_, { startYear, endYear }) => {
      try {
        return await Film.find({
          year: { $gte: startYear, $lte: endYear }
        }).limit(50).sort({ year: 1 });
      } catch (error) {
        throw new Error('Error fetching films by year range: ' + error.message);
      }
    },

    topRatedFilms: async (_, { limit = 10 }) => {
      try {
        return await Film.find({
          'imdb.rating': { $exists: true, $ne: null }
        })
        .sort({ 'imdb.rating': -1 })
        .limit(limit);
      } catch (error) {
        throw new Error('Error fetching top rated films: ' + error.message);
      }
    }
  },

  Mutation: {
    addFilm: async (_, args) => {
      try {
        const film = new Film(args);
        return await film.save();
      } catch (error) {
        throw new Error('Error adding film: ' + error.message);
      }
    },

    updateFilm: async (_, { id, ...updates }) => {
      try {
        const film = await Film.findByIdAndUpdate(
          id,
          { $set: updates },
          { new: true, runValidators: true }
        );
        
        if (!film) {
          throw new Error('Film not found');
        }
        
        return film;
      } catch (error) {
        throw new Error('Error updating film: ' + error.message);
      }
    },

    deleteFilm: async (_, { id }) => {
      try {
        const result = await Film.findByIdAndDelete(id);
        return !!result;
      } catch (error) {
        throw new Error('Error deleting film: ' + error.message);
      }
    }
  }
};

module.exports = resolvers;