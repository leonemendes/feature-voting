#!/bin/bash

# Feature Voting System Run Script
# Starts both backend and frontend servers

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

# Check if virtual environment exists
check_setup() {
    if [[ ! -d "backend/venv" ]]; then
        print_error "Virtual environment not found. Please run ./setup.sh first."
        exit 1
    fi
    
    if [[ ! -d "frontend/node_modules" ]]; then
        print_error "Node modules not found. Please run ./setup.sh first."
        exit 1
    fi
}

# Kill background processes on exit
cleanup() {
    print_step "Stopping servers..."
    if [[ -n $BACKEND_PID ]]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [[ -n $FRONTEND_PID ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    print_success "Servers stopped"
}

# Handle script interruption
trap cleanup INT TERM EXIT

# Main function
main() {
    print_header "Feature Voting System - Starting Servers"
    
    # Check if setup has been run
    check_setup
    
    # Start backend server
    print_step "Starting Flask backend server..."
    cd backend
    source venv/bin/activate
    python app.py &
    BACKEND_PID=$!
    cd ..
    print_success "Backend server started (PID: $BACKEND_PID)"
    
    # Wait a moment for backend to start
    sleep 2
    
    # Start frontend server
    print_step "Starting React Native frontend server..."
    cd frontend
    npx expo start -c &
    FRONTEND_PID=$!
    cd ..
    print_success "Frontend server started (PID: $FRONTEND_PID)"
    
    print_header "Servers Running"
    echo -e "${GREEN}🚀 Backend server: http://localhost:5000${NC}"
    echo -e "${GREEN}🚀 Frontend server: http://localhost:19006${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
    
    # Wait for processes to finish
    wait
}

# Run main function
main "$@"