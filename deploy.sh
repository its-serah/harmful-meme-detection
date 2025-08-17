#!/bin/bash

# Harmful Meme Detection API Deployment Script
# This script builds and deploys the Docker container

set -e

echo "Starting Harmful Meme Detection API Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "WARNING: Docker Compose is not installed. Using docker compose command..."
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Parse command line arguments
ACTION=${1:-"up"}
DETACHED=""

if [ "$2" == "-d" ] || [ "$2" == "--detach" ]; then
    DETACHED="-d"
fi

case $ACTION in
    up|start)
        echo "Building and starting containers..."
        $COMPOSE_CMD up --build $DETACHED
        if [ -n "$DETACHED" ]; then
            echo "Application is running at http://localhost:5000"
            echo "Check logs with: $COMPOSE_CMD logs -f"
        fi
        ;;
    
    down|stop)
        echo "Stopping containers..."
        $COMPOSE_CMD down
        echo "Containers stopped"
        ;;
    
    restart)
        echo "Restarting containers..."
        $COMPOSE_CMD restart
        echo "Containers restarted"
        ;;
    
    logs)
        echo "Showing logs..."
        $COMPOSE_CMD logs -f
        ;;
    
    build)
        echo "Building Docker image..."
        docker build -t harmful-meme-detector .
        echo "Image built successfully"
        ;;
    
    test)
        echo "Testing the API..."
        # Start container in background
        $COMPOSE_CMD up -d
        
        # Wait for container to be ready
        echo "Waiting for container to be ready..."
        sleep 10
        
        # Test health endpoint
        echo "Testing /health endpoint..."
        curl -f http://localhost:5000/health || (echo "Health check failed" && exit 1)
        echo ""
        
        # Test info endpoint
        echo "Testing /info endpoint..."
        curl -f http://localhost:5000/info || (echo "Info endpoint failed" && exit 1)
        echo ""
        
        echo "All tests passed!"
        
        # Stop container
        $COMPOSE_CMD down
        ;;
    
    push)
        echo "Pushing to Docker Hub..."
        if [ -z "$DOCKER_USERNAME" ]; then
            echo "ERROR: DOCKER_USERNAME environment variable not set"
            exit 1
        fi
        docker tag harmful-meme-detector:latest $DOCKER_USERNAME/harmful-meme-detector:latest
        docker push $DOCKER_USERNAME/harmful-meme-detector:latest
        echo "Image pushed to Docker Hub"
        ;;
    
    *)
        echo "Usage: ./deploy.sh [up|down|restart|logs|build|test|push] [-d|--detach]"
        echo ""
        echo "Commands:"
        echo "  up, start    - Build and start containers"
        echo "  down, stop   - Stop and remove containers"
        echo "  restart      - Restart containers"
        echo "  logs         - Show container logs"
        echo "  build        - Build Docker image only"
        echo "  test         - Run API tests"
        echo "  push         - Push image to Docker Hub"
        echo ""
        echo "Options:"
        echo "  -d, --detach - Run containers in background"
        exit 1
        ;;
esac
