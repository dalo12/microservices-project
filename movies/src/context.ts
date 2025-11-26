import { MongoClient } from 'mongodb';
import { Context } from 'apollo-server-core';

export interface MyContext extends Context {
  db: MongoClient;
}

export const createContext = async (): Promise<MyContext> => {
  const client = new MongoClient(process.env.MONGODB_URI || '', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  await client.connect();

  return {
    db: client,
  };
};