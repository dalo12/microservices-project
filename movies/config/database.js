const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    // Assuming MongoDB is running on default port 27017
    // If using Docker, it might be localhost:27017
    const databaseConnectionString = process.env.DATABASE_CONN_STRING || 'mongodb://admin:12345@localhost:27017/sample_mflix?authSource=admin';

    const conn = await mongoose.connect(databaseConnectionString);
    
    console.log(`MongoDB Connected: ${conn.connection.host}`);

    // Verify we can actually query data
    const Film = require('../models/Film');
    const count = await Film.countDocuments();
    console.log(`🎬 Total films in database: ${count}`);
    
  } catch (error) {
    console.error('Database connection error:', error);
    process.exit(1);
  }
};

module.exports = connectDB;