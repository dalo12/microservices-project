import { MongoClient } from 'mongodb';
import { config } from '../config';

let db: any;

export const connectToDatabase = async () => {
    if (db) {
        return db;
    }

    const client = new MongoClient(config.MONGODB_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    });

    await client.connect();
    db = client.db(config.DB_NAME);
    return db;
};