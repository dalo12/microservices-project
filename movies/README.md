# MFlix GraphQL Service

This project is a GraphQL service for the MFlix sample database, built using TypeScript and Apollo Server. It connects to a MongoDB database and provides an API endpoint for querying movie data.

## Project Structure

- **src/**: Contains the source code for the application.
  - **index.ts**: Entry point of the application, initializes the server and connects to MongoDB.
  - **server.ts**: Sets up the Apollo Server with the GraphQL schema and middleware.
  - **context.ts**: Creates the context for the GraphQL server, providing access to the database.
  - **schema/**: Contains GraphQL type definitions and resolvers.
    - **typeDefs.graphql**: GraphQL type definitions for the API.
    - **resolvers.ts**: Resolvers for GraphQL queries and mutations.
  - **models/**: Contains Mongoose models for MongoDB.
    - **movie.model.ts**: Defines the Movie model schema.
  - **loaders/**: Contains functions for loading and connecting to services.
    - **mongodb.ts**: Establishes a connection to the MongoDB database.
  - **config/**: Contains configuration settings for the application.
    - **index.ts**: Exports configuration settings.
  - **utils/**: Contains utility functions.
    - **logger.ts**: Logger utility for logging messages and errors.

- **scripts/**: Contains scripts for managing the database.
  - **import-mflix.sh**: Shell script to import MFlix sample data into MongoDB.

- **Dockerfile**: Instructions for building the Docker image for the application.

- **docker-compose.yml**: Defines services, networks, and volumes for running the application with Docker Compose.

- **.dockerignore**: Specifies files and directories to ignore when building the Docker image.

- **.env.example**: Example of environment variables needed for the application.

- **package.json**: Configuration file for npm, listing dependencies and scripts.

- **tsconfig.json**: TypeScript configuration file specifying compiler options.

## Getting Started

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd mflix-graphql-service
   ```

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Set up environment variables**:
   Copy `.env.example` to `.env` and configure the necessary environment variables.

4. **Run the application**:
   ```
   npm run start
   ```

5. **Access the GraphQL API**:
   The API will be available at `http://localhost:4000/graphql`.

## Importing Sample Data

To import the MFlix sample data into MongoDB, run the following command:
```
bash scripts/import-mflix.sh
```

## License

This project is licensed under the MIT License.