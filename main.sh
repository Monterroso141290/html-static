#!/bin/bash
echo "Starting the application..."

# Step 1: Generate the site from project root
python3 src/main.py

# Step 2: Move into the public directory (which now exists)
cd public || { echo "Error: public directory not found"; exit 1; }

# Step 3: Start the HTTP server
echo "Serving on http://localhost:8888"
python3 -m http.server 8888
