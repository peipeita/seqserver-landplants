# Multi-architecture Dockerfile for SequenceServer
FROM --platform=$BUILDPLATFORM ruby:3.2-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ncbi-blast+ \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install SequenceServer v3.1.2 (tree widget works in this version)
RUN gem install sequenceserver -v 3.1.2

# Create directories
RUN mkdir -p /app/blast_dbs /app/config /app/scripts

# Set working directory
WORKDIR /app

# Copy configuration and scripts
COPY config/sequenceserver.conf /app/config/
COPY scripts/ /app/scripts/

# Create a dummy .sequenceserver.conf to skip email prompt
RUN mkdir -p /root && echo "---\n:email: ''" > /root/.sequenceserver.conf

# Expose port
EXPOSE 4567

# Set environment variables
ENV SEQUENCESERVER_CONFIG=/app/config/sequenceserver.conf

# Run SequenceServer
CMD ["sequenceserver", "-c", "/app/config/sequenceserver.conf"]
