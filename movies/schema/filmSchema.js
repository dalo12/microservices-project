const { gql } = require('apollo-server-express');

const typeDefs = gql`
  type Film {
    _id: ID!
    title: String!
    year: Int!
    runtime: Int
    released: String
    plot: String
    fullplot: String
    type: String
    directors: [String]
    cast: [String]
    countries: [String]
    genres: [String]
    imdb: IMDB
    tomatoes: Tomatoes
    awards: Awards
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

  type Mutation {
    # Add a new film
    addFilm(
      title: String!
      year: Int!
      runtime: Int
      plot: String
      directors: [String]
      cast: [String]
      genres: [String]
    ): Film
    
    # Update an existing film
    updateFilm(
      id: ID!
      title: String
      year: Int
      runtime: Int
      plot: String
      directors: [String]
      cast: [String]
      genres: [String]
    ): Film
    
    # Delete a film
    deleteFilm(id: ID!): Boolean
  }
`;

module.exports = typeDefs;