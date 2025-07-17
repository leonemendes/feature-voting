#!/bin/bash

IMAGE_NAME="claude-code-env"
PROJECT_DIR="$(pwd)"

if [ "$1" == "--rebuild" ]; then
    echo "♻️ Rebuilding Docker image..."
    docker build -t $IMAGE_NAME .
else
    if ! docker image inspect $IMAGE_NAME > /dev/null 2>&1; then
        echo "📦 Building image for the first time..."
        docker build -t $IMAGE_NAME .
    else
        echo "✅ Using existing image: $IMAGE_NAME"
    fi
fi

echo "🚀 Starting container..."
docker run -it --rm \
    -v "$PROJECT_DIR":/workspace \
    $IMAGE_NAME