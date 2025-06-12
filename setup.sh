#!/bin/bash
set -e  # Exit on error

# Create necessary directories
mkdir -p output
mkdir -p .chroma_cache
mkdir -p .chroma_db

# Install system dependencies (for ChromaDB)
if command -v apt-get >/dev/null; then
    # For Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libsqlite3-dev \
        libpq-dev \
        libssl-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        libjpeg-dev \
        libpng-dev \
        libopenblas-dev \
        liblapack-dev \
        gfortran \
        && rm -rf /var/lib/apt/lists/*
fi

# Install Python dependencies
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Install ChromaDB with specific backends
pip install --no-cache-dir \
    chromadb \
    sentence-transformers \
    pypdf \
    pydantic>=2.0.0

# Set environment variables
echo "CHROMA_DB_IMPL=duckdb+parquet" >> $GITHUB_ENV
echo "CHROMA_CACHE_DIR=.chroma_cache" >> $GITHUB_ENV
echo "CHROMA_ANONYMIZED_TELEMETRY=False" >> $GITHUB_ENV
