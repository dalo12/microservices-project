const { gql } = require('apollo-server-express');

const typeDefs = gql`
  type Film {
    _id: ID!
    plot: String
    genres: [String]
    runtime: Int
    cast: [String]
    poster: String
    title: String!
    fullplot: String
    languages: [String]
    released: String
    directors: [String]
    rated: String
    awards: Awards
    year: Int
    imdb: IMDB
    countries: [String]
    type: String
    tomatoes: Tomatoes
    num_mflix_comments: Int
  }

  type IMDB {
    rating: Float
    votes: Int
    id: Int
  }

  type Tomatoes {
    viewer: TomatoRating
    critic: TomatoRating
    lastUpdated: String
  }

  type TomatoRating {
    rating: Float
    numReviews: Int
    meter: Int
  }

  type Awards {
    wins: Int
    nominations: Int
    text: String
  }

  input FilmFilter {
    _id: ID
    title: String
    year: Int
    genre: String
    director: String
    cast: String
  }

  type Query {
    # Get all films with optional filtering and pagination
    films(
      limit: Int
      skip: Int
      filter: FilmFilter
    ): [Film]
    
    # Get film by ID
    film(id: ID!): Film
    
    # Search films by title
    searchFilms(title: String!): [Film]
    
    # Get films by genre
    filmsByGenre(genre: String!): [Film]
    
    # Get films by year range
    filmsByYearRange(startYear: Int!, endYear: Int!): [Film]
    
    # Get top rated films
    topRatedFilms(limit: Int): [Film]
  }
`;

module.exports = typeDefs;