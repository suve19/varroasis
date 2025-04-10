#!/bin/bash

# Configuration
DITTO_HOST="http://localhost:8080"
USERNAME="ditto"
PASSWORD="ditto"

# JSON file paths
THING_FILE="camera-thing.json"
POLICY_FILE="camera-policy.json"
CONNECTIVITY_FILE="ditto-http-connection.json"

# Thing and Policy IDs from the thing and policy JSON
THING_ID=$(jq -r '.thingId' "$THING_FILE")
POLICY_ID=$(jq -r '.policyId' "$POLICY_FILE")
CONNECTION_ID=$(jq -r '.id' "$CONNECTIVITY_FILE")



# Post Policy
echo "Posting Policy: $POLICY_ID"
curl -i -X PUT "$DITTO_HOST/api/2/policies/$POLICY_ID" \
  -u "$USERNAME:$PASSWORD" \
  -H 'Content-Type: application/json' \
  -d @"$POLICY_FILE"

echo -e "\n---"


# Post Thing
echo "Posting Thing: $THING_ID"
curl -i -X PUT "$DITTO_HOST/api/2/things/$THING_ID" \
  -u "$USERNAME:$PASSWORD" \
  -H 'Content-Type: application/json' \
  -d @"$THING_FILE"

echo -e "\n---"



# # Post Connectivity Connection
# echo "Posting Connectivity Connection: $CONNECTION_ID"
# curl -i -X PUT "$DITTO_HOST/api/2/connectivity/connections/$CONNECTION_ID" \
#   -u "$USERNAME:$PASSWORD" \
#   -H 'Content-Type: application/json' \
#   -d @"$CONNECTIVITY_FILE"

echo -e "\n--- All Done ---"
