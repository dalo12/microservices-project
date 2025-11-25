# --- Stage 1: Download and Prepare Data ---
FROM ubuntu:22.04 AS data_preparer

# Install necessary tools
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install MongoDB Database Tools
RUN curl https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2204-x86_64-100.13.0.deb -o mongodb-database-tools.deb
RUN dpkg -i mongodb-database-tools.deb

WORKDIR /tmp/mflix_setup

# Download the MFlix sample data
RUN curl https://atlas-education.s3.amazonaws.com/sampledata.archive -o sampledata.archive

# --- Stage 2: Final MongoDB Image ---
FROM mongo:latest AS database

# Copy the prepared data from the first stage
COPY --from=data_preparer /tmp/mflix_setup/ /tmp/mflix_setup/

# Copy the custom scripts
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY import-mflix.js /docker-entrypoint-initdb.d/import-mflix.js

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the custom entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]