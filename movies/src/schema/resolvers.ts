import { IResolvers } from 'graphql-tools';
import Movie from '../models/movie.model';

const resolvers: IResolvers = {
  Query: {
    movies: async () => {
      return await Movie.find();
    },
    movie: async (_: any, { id }: { id: string }) => {
      return await Movie.findById(id);
    },
  },
  Mutation: {
    addMovie: async (_: any, { input }: { input: any }) => {
      const movie = new Movie(input);
      return await movie.save();
    },
    updateMovie: async (_: any, { id, input }: { id: string; input: any }) => {
      return await Movie.findByIdAndUpdate(id, input, { new: true });
    },
    deleteMovie: async (_: any, { id }: { id: string }) => {
      return await Movie.findByIdAndRemove(id);
    },
  },
};

export default resolvers;