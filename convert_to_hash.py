import json
import hashlib

# Load the token store
with open('token_store.json', 'r') as f:
    token_store = json.load(f)

# Create a new dict with hashed tokens
hashed_token_store = {}
for token, data in token_store.items():
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    hashed_token_store[hashed_token] = data

# Overwrite the original file
with open('token_store.json', 'w') as f:
    json.dump(hashed_token_store, f, indent=4)

print("✅ token_store.json has been updated with hashed tokens.")