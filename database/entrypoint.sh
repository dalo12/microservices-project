#!/bin/bash
set -e

# The flag file path is set via an environment variable in docker-compose.yml
MFLIX_IMPORTED_FLAG=${MFLIX_IMPORTED_FLAG:-/data/mflix_imported}

# Check if the data has already been imported (i.e., if the flag file exists)
if [ ! -f "$MFLIX_IMPORTED_FLAG" ]; then
    echo "--- Data import flag not found. Running initial data import. ---"
    
    # 1. Run the MongoDB server in the background (headless)
    mongod --fork --logpath /dev/null

    # 2. Execute the import script using mongo-shell
    # The import-mflix.js script will handle the 'mongoimport' commands.
    /usr/bin/mongosh --file /docker-entrypoint-initdb.d/import-mflix.js

    # 3. Stop the background server
    mongod --shutdown

    # 4. Create the flag file to indicate successful import
    touch "$MFLIX_IMPORTED_FLAG"
    echo "--- Data import complete. Flag file created: $MFLIX_IMPORTED_FLAG ---"
else
    echo "--- Data import flag found. Skipping initial data import. ---"
fi

# Finally, execute the main MongoDB server command (the original entrypoint command)
exec docker-entrypoint.sh "$@"