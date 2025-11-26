import { ApolloServer } from 'apollo-server';
import { loadSchema } from './schema/typeDefs.graphql';
import { resolvers } from './schema/resolvers';
import { createContext } from './context';
import { connectToDatabase } from './loaders/mongodb';
import { config } from './config';

const startServer = async () => {
    const db = await connectToDatabase();
    
    const server = new ApolloServer({
        typeDefs: loadSchema(),
        resolvers,
        context: () => createContext(db),
    });

    server.listen({ port: config.PORT }).then(({ url }) => {
        console.log(`🚀 Server ready at ${url}`);
    });
};

startServer().catch(error => {
    console.error('Error starting server:', error);
});