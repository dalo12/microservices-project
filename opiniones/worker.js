const amqp = require('amqplib');
const mongoose = require('mongoose');

const RABBITMQ_URL = process.env.RABBITMQ_URL || 'amqp://rabbitmq';
const QUEUE_NAME = 'ratings_queue';
const DATABASE_CONN_STRING = process.env.DATABASE_CONN_STRING || 'mongodb://admin:12345@database:27017/ratings_db?authSource=admin';

// MongoDB Schema
const ratingSchema = new mongoose.Schema({
    email: String,
    movieId: String,
    rating: Number,
    comment: String,
    timestamp: Date
});

const Rating = mongoose.model('Rating', ratingSchema);

async function connectMongoDB() {
    try {
        await mongoose.connect(DATABASE_CONN_STRING);
        console.log('Connected to MongoDB');
    } catch (error) {
        console.error('Error connecting to MongoDB:', error);
        setTimeout(connectMongoDB, 5000);
    }
}

async function startWorker() {
    await connectMongoDB();

    try {
        const connection = await amqp.connect(RABBITMQ_URL);
        const channel = await connection.createChannel();
        await channel.assertQueue(QUEUE_NAME, { durable: true });

        console.log('Waiting for messages in %s', QUEUE_NAME);

        channel.consume(QUEUE_NAME, async (msg) => {
            if (msg !== null) {
                const content = JSON.parse(msg.content.toString());
                console.log('Received rating:', content);

                try {
                    const newRating = new Rating(content);
                    await newRating.save();
                    console.log('Rating saved to database');
                    channel.ack(msg);
                } catch (dbError) {
                    console.error('Error saving to database:', dbError);
                    // Optionally nack or retry logic here
                }
            }
        });
    } catch (error) {
        console.error('Error connecting to RabbitMQ:', error);
        setTimeout(startWorker, 5000);
    }
}

startWorker();
