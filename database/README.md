# Database

Database implementation using MongoDB, using MFlix sample database.

To download the sample dabatase
    
    $ curl  https://atlas-education.s3.amazonaws.com/sampledata.archive -o sampledata.archive

To import it

    $ mongorestore --username admin --password 12345 --authenticationDatabase admin --archive=sampledata.archive --port=27017

Note: you need the MongoDB Command Line Database Tools. You can download it from [MongoDB Download Center](https://www.mongodb.com/try/download/database-tools) and install it (in Fedora 42) using

    # dnf install ./mongodb-database-tools-<os-version>-<arch>-X.Y.Z.rpm

Finally, to check if the import worked log into the MongoDB service using

    $ mongosh "mongodb://admin:12345@localhost:27017/mflix?authSource=admin"