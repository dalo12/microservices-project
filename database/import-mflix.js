// This file is executed by mongosh in the entrypoint.sh script

// Use a temporary database name for connection
db = db.getSiblingDB('admin');

// 1. Run the core import commands
// This command will execute shell commands from the MongoDB image.
// We use the JSON files prepared in the Dockerfile's first stage.

print('Starting data import for MFlix database...');

runProgram('mongorestore', 
    '--username', 'admin',
    '--password', '12345',
    '--authenticationDatabase', 'admin',
    '--archive=sampledata.archive', 
    '--port=27017')

// Import comments collection
runProgram(
  'mongoimport',
  '--db', 'mflix',
  '--collection', 'comments',
  '--drop',
  '--file', '/tmp/mflix_setup/comments.json'
);

// Import movies collection
runProgram(
  'mongoimport',
  '--db', 'mflix',
  '--collection', 'movies',
  '--drop',
  '--file', '/tmp/mflix_setup/movies.json'
);

// Import sessions collection
runProgram(
  'mongoimport',
  '--db', 'mflix',
  '--collection', 'sessions',
  '--drop',
  '--file', '/tmp/mflix_setup/sessions.json'
);

// Import users collection
runProgram(
  'mongoimport',
  '--db', 'mflix',
  '--collection', 'users',
  '--drop',
  '--file', '/tmp/mflix_setup/users.json'
);

print('MFlix data import finished.');