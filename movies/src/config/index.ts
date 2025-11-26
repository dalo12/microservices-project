import dotenv from 'dotenv';

dotenv.config();

const config = {
  mongoURI: process.env.MONGO_URI || 'mongodb://localhost:27017/mflix',
  port: process.env.PORT || 4000,
  jwtSecret: process.env.JWT_SECRET || 'your_jwt_secret',
};

export default config;