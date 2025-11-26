#!/bin/bash

# Download the MFlix sample data if it doesn't already exist
if [ ! -f sampledata.archive ]; then
    echo "Downloading MFlix sample data..."
    curl https://atlas-education.s3.amazonaws.com/sampledata.archive -o sampledata.archive
else
    echo "MFlix sample data already exists. Skipping download."
fi

# Import the sample data into MongoDB
echo "Importing MFlix sample data into MongoDB..."
mongorestore --username admin --password 12345 --authenticationDatabase admin --archive=sampledata.archive --port=27017

echo "Import completed."