#!/bin/bash

IMAGE_NAME="claude-code-env"

PROJECT_DIR="$(pwd)"

#echo "🚀 Building docker image..."
#docker build -t $IMAGE_NAME .

echo "✅ Running container with Claude Code..."
docker run -it --rm \
  -v "$PROJECT_DIR":/workspace \
  $IMAGE_NAME