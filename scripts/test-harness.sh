#!/bin/bash

# Usage: 
#   Defaults the Base URL and Number of Iterations ./test-harness.sh
#   Only passing the number of iterations ./test-harness.sh "" 150
#   Only passing the Base URL ./test-harness.sh http://your.custom.url


# Default number of iterations
DEFAULT_ITERATIONS=100

# Use provided URL and iterations if given, else use defaults
BASE_URL="${1:-$DEFAULT_BASE_URL}"
ITERATIONS="${2:-$DEFAULT_ITERATIONS}"

# Use provided URL if given, else use default
BASE_URL="${1:-$DEFAULT_BASE_URL}"

# Get current timestamp
timestamp=$(date +"%Y%m%d_%H%M%S")

# Ensure the logs directory exists
mkdir -p /logs/requests

# Arrays to store result URLs and request IDs
declare -a urls=()
declare -a requestids=()

# Function to generate a random float between min and max
rand_float() {
    min="$1"
    max="$2"
    awk -v min="$min" -v max="$max" -v seed="$RANDOM" 'BEGIN{srand(seed); printf("%.6f", min+rand()*(max-min))}'
}

# Function to generate a random integer between min and max
rand_int() {
    shuf -i "$1"-"$2" -n 1
}

# Endpoint URL
ENDPOINT='${BASE_URL}/predict'

# Generate and submit 100 random samples
for i in $(seq 1 "${ITERATIONS}"); do
    # Generate random features
    Rooms=$(rand_int 1 5)
    Bathroom=$(rand_int 1 3)
    Landsize=$(rand_int 100 350)
    Latitude=$(rand_float -39.2514 -36.3514)
    Longitude=$(rand_float 143.1858 146.8058)

    # Create JSON data
    JSON_DATA=$(jq -n \
        --argjson rooms "$Rooms" \
        --argjson bathroom "$Bathroom" \
        --argjson landsize "$Landsize" \
        --argjson latitude "$Latitude" \
        --argjson longitude "$Longitude" \
        '{"features": [$rooms, $bathroom, $landsize, $latitude, $longitude]}')

    # Submit POST request
    RESPONSE=$(curl -s -X 'POST' "$ENDPOINT" -H 'accept: application/json' -d "$JSON_DATA")

    # Extract result URL and request ID from response
    RESULT_URL=$(echo "$RESPONSE" | jq -r '.results')
    REQUESTID=$(basename "$RESULT_URL")

    # Store in arrays
    urls+=("$RESULT_URL")
    requestids+=("$REQUESTID")
done

# Initialize pending arrays
pending_urls=("${urls[@]}")
pending_requestids=("${requestids[@]}")

# Write pending_urls and pending_requestids to timestamped files
printf "%s\n" "${pending_urls[@]}" > /logs/pending_urls_${timestamp}.txt"
printf "%s\n" "${pending_requestids[@]}" > /logs/pending_requestids_${timestamp}.txt"

# Iterate over pending URLs
while [ ${#pending_urls[@]} -gt 0 ]; do
    new_pending_urls=()
    new_pending_requestids=()

    for index in "${!pending_urls[@]}"; do
        URL="${pending_urls[index]}"
        REQUESTID="${pending_requestids[index]}"

        # Submit GET request
        RESPONSE=$(curl -s -X 'GET' "${BASE_URL}${URL}" -H 'accept: application/json')

        # Check the message field
        MESSAGE=$(echo "$RESPONSE" | jq -r '.results.message')

        if [ "$MESSAGE" == "Complete" ]; then
            # Save response to file
            echo "$RESPONSE" > "/logs/requests/$REQUESTID.json"
        else
            # Keep pending if not complete
            new_pending_urls+=("$URL")
            new_pending_requestids+=("$REQUESTID")
        fi
    done

    # Update pending arrays
    pending_urls=("${new_pending_urls[@]}")
    pending_requestids=("${new_pending_requestids[@]}")

    # Wait before next iteration
    sleep 1
done
