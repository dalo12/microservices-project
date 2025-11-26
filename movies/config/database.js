const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    // Assuming MongoDB is running on default port 27017
    // If using Docker, it might be localhost:27017
    const conn = await mongoose.connect('mongodb://localhost:27017/sample_mflix', {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error('Database connection error:', error);
    process.exit(1);
  }
};

module.exports = connectDB;