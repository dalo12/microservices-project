import { ApolloServer } from 'apollo-server';
import { connectToDatabase } from './loaders/mongodb';
import { typeDefs } from './schema/typeDefs.graphql';
import { resolvers } from './schema/resolvers';
import { createContext } from './context';
import config from './config';

const startServer = async () => {
    // Connect to MongoDB
    await connectToDatabase();

    // Initialize Apollo Server
    const server = new ApolloServer({
        typeDefs,
        resolvers,
        context: createContext,
    });

    // Start the server
    const { url } = await server.listen({ port: config.PORT });
    console.log(`🚀 Server ready at ${url}`);
};

// Start the application
startServer().catch(error => {
    console.error('Error starting the server:', error);
});