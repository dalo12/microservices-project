const express = require('express');
const { ApolloServer } = require('apollo-server-express');
const connectDB = require('./config/database');
const typeDefs = require('./schema/filmSchema');
const resolvers = require('./resolvers/filmResolvers');

// Connect to database
connectDB();

async function startServer() {
  const app = express();
  
  // Basic middleware
  app.use(express.json());
  
  // Create Apollo Server
  const server = new ApolloServer({
    typeDefs,
    resolvers,
    context: ({ req }) => {
      return { req };
    },
    formatError: (error) => {
      console.error('GraphQL Error:', error);
      
      // Don't expose internal errors in production
      if (process.env.NODE_ENV === 'production') {
        const { message, extensions } = error;
        return {
          message,
          code: extensions?.code || 'INTERNAL_SERVER_ERROR',
        };
      }
      
      return error;
    },
    introspection: process.env.NODE_ENV !== 'production', // Disable in production
    playground: process.env.NODE_ENV !== 'production', // Disable in production
  });

  await server.start();
  
  // Apply Apollo GraphQL middleware to Express
  server.applyMiddleware({ 
    app, 
    path: '/graphql',
    cors: {
      origin: process.env.ALLOWED_ORIGINS || '*',
      credentials: true,
    }
  });

  // Enhanced health check route
  app.get('/health', (req, res) => {
    const status = mongoose.connection.readyState === 1 ? 'healthy' : 'unhealthy';
    
    res.status(200).json({ 
      status: 'OK', 
      message: 'GraphQL Films API is running',
      database: status,
      timestamp: new Date().toISOString()
    });
  });

  // Root route
  app.get('/', (req, res) => {
    res.json({
      message: 'GraphQL Films API',
      graphqlEndpoint: '/graphql',
      healthCheck: '/health',
      version: '1.0.0'
    });
  });

  const PORT = process.env.PORT || 4000;
  const HOST = process.env.HOST || '0.0.0.0';
  
  app.listen(PORT, HOST, () => {
    console.log(`🚀 Server ready at http://${HOST}:${PORT}${server.graphqlPath}`);
    console.log(`📊 Health check at http://${HOST}:${PORT}/health`);
    console.log(`🏠 Root endpoint at http://${HOST}:${PORT}/`);
    console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
  });
}

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n👋 Received SIGINT. Shutting down gracefully...');
  await mongoose.connection.close();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('👋 Received SIGTERM. Shutting down gracefully...');
  await mongoose.connection.close();
  process.exit(0);
});

startServer().catch(error => {
  console.error('Failed to start server:', error);
  process.exit(1);
});