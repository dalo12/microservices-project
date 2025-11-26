const express = require('express');
const { ApolloServer } = require('apollo-server-express');
const connectDB = require('./config/database');
const typeDefs = require('./schema/filmSchema');
const resolvers = require('./resolvers/filmResolvers');

// Connect to database
connectDB();

async function startServer() {
  const app = express();
  
  // Create Apollo Server
  const server = new ApolloServer({
    typeDefs,
    resolvers,
    context: ({ req }) => {
      // You can add authentication context here
      return { req };
    },
    formatError: (error) => {
      // Don't give the specific errors to the client
      console.error(error);
      return {
        message: error.message,
        code: error.extensions?.code || 'INTERNAL_SERVER_ERROR',
      };
    }
  });

  await server.start();
  
  // Apply Apollo GraphQL middleware to Express
  server.applyMiddleware({ app, path: '/graphql' });

  // Basic health check route
  app.get('/health', (req, res) => {
    res.status(200).json({ status: 'OK', message: 'GraphQL Films API is running' });
  });

  const PORT = process.env.PORT || 4000;
  
  app.listen(PORT, () => {
    console.log(`🚀 Server ready at http://localhost:${PORT}${server.graphqlPath}`);
    console.log(`📊 Health check at http://localhost:${PORT}/health`);
  });
}

startServer().catch(error => {
  console.error('Failed to start server:', error);
});