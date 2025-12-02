const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const amqp = require('amqplib');

const app = express();
const port = 5001;

// Enable CORS for all routes
app.use(cors());

app.use(bodyParser.json());

const RABBITMQ_URL = process.env.RABBITMQ_URL || 'amqp://rabbitmq';
const QUEUE_NAME = 'ratings_queue';

let channel;

async function connectRabbitMQ() {
  try {
    const connection = await amqp.connect(RABBITMQ_URL);
    channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME, { durable: true });
    console.log('Connected to RabbitMQ');
  } catch (error) {
    console.error('Error connecting to RabbitMQ:', error);
    setTimeout(connectRabbitMQ, 5000); // Retry after 5 seconds
  }
}

connectRabbitMQ();

app.post('/ratings', async (req, res) => {
  const { email, movieId, rating, comment } = req.body;

  if (!email || !movieId || !rating) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const ratingData = { email, movieId, rating, comment, timestamp: new Date() };

  try {
    if (channel) {
      channel.sendToQueue(QUEUE_NAME, Buffer.from(JSON.stringify(ratingData)), { persistent: true });
      console.log('Rating sent to queue:', ratingData);
      res.status(201).json({ message: 'Rating received and processing' });
    } else {
      res.status(503).json({ error: 'Service unavailable (Queue not connected)' });
    }
  } catch (error) {
    console.error('Error sending message to queue:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`Calificacion service listening at http://localhost:${port}`);
});
