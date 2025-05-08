#!/bin/bash

# Script to generate RSA key pair and format them with "\n" instead of actual newlines
# Usage: ./generate-keys.sh

# Path for the key files
PRIVATE_KEY_FILE="private.key"
PUBLIC_KEY_FILE="public.key"
PRIVATE_KEY_ONELINE="private_key_oneline.txt"
PUBLIC_KEY_ONELINE="public_key_oneline.txt"

echo "Generating RSA key pair..."

# Generate private key (2048 bits)
openssl genpkey -algorithm RSA -out "$PRIVATE_KEY_FILE" -pkeyopt rsa_keygen_bits:2048
if [ $? -ne 0 ]; then
    echo "Error generating private key"
    exit 1
fi

# Extract public key from private key
openssl rsa -in "$PRIVATE_KEY_FILE" -pubout -out "$PUBLIC_KEY_FILE"
if [ $? -ne 0 ]; then
    echo "Error extracting public key"
    exit 1
fi

echo "Keys generated successfully"
echo "- Private key: $PRIVATE_KEY_FILE"
echo "- Public key: $PUBLIC_KEY_FILE"

# Create one-line versions with "\n" instead of actual newlines
echo "Creating one-line versions with '\\n' instead of newlines..."

# Convert private key to one line with \n
cat "$PRIVATE_KEY_FILE" | awk '{printf("%s\\n", $0)}' > "$PRIVATE_KEY_ONELINE"
echo "- One-line private key: $PRIVATE_KEY_ONELINE"

# Convert public key to one line with \n
cat "$PUBLIC_KEY_FILE" | awk '{printf("%s\\n", $0)}' > "$PUBLIC_KEY_ONELINE"
echo "- One-line public key: $PUBLIC_KEY_ONELINE"

# Make the original key files readable but not writable by owner only
chmod 400 "$PRIVATE_KEY_FILE"
chmod 444 "$PUBLIC_KEY_FILE"

echo "Done!"
