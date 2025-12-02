const Film = require('../models/Film');

const resolvers = {
  Query: {
    films: async (_, { limit = 10, skip = 0, filter = {} }) => {
      try {
        let query = {};
        
        if (filter._id) {
          query._id = filter._id;
        }
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

        let results = await Film.find(query)
          .limit(limit)
          .skip(skip)
          .sort({ year: -1 });

        if(results.length === 1) {
          console.log(`Fetched ${JSON.stringify(results)} with filter: ${JSON.stringify(filter)}`);
        }

        return results;
      } catch (error) {
        throw new Error('Error fetching films: ' + error.message);
      }
    },

    film: async (_, { id }) => {
      try {
        const film = await Film.findById(id);
        if (!film || !film.poster) {
          throw new Error('Film not found or has no poster');
        }
        return film;
      } catch (error) {
        throw new Error('Error fetching film: ' + error.message);
      }
    },

    searchFilms: async (_, { title }) => {
      try {
        return await Film.find({
          title: { $regex: title, $options: 'i' },
          poster: { $exists: true, $ne: null }
        }).limit(20);
      } catch (error) {
        throw new Error('Error searching films: ' + error.message);
      }
    },

    filmsByGenre: async (_, { genre }) => {
      try {
        return await Film.find({
          genres: { $in: [genre] },
          poster: { $exists: true, $ne: null }
        }).limit(20).sort({ 'imdb.rating': -1 });
      } catch (error) {
        throw new Error('Error fetching films by genre: ' + error.message);
      }
    },

    filmsByYearRange: async (_, { startYear, endYear }) => {
      try {
        return await Film.find({
          year: { $gte: startYear, $lte: endYear },
          poster: { $exists: true, $ne: null }
        }).limit(50).sort({ year: 1 });
      } catch (error) {
        throw new Error('Error fetching films by year range: ' + error.message);
      }
    },

    topRatedFilms: async (_, { limit = 10 }) => {
      try {
        return await Film.find({
          'imdb.rating': { $exists: true, $ne: null },
          poster: { $exists: true, $ne: null }
        })
        .sort({ 'imdb.rating': -1 })
        .limit(limit);
      } catch (error) {
        throw new Error('Error fetching top rated films: ' + error.message);
      }
    }
  },
};

module.exports = resolvers;