#!/bin/bash

# Feature Voting System Setup Script
# Sets up backend Python environment and frontend Node.js environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_step() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main setup function
main() {
    print_header "Feature Voting System Setup"
    
    # Check if we're in the right directory
    if [[ ! -f "setup.sh" ]]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Backend setup
    print_header "Backend Setup (Python)"
    setup_backend
    
    # Frontend setup
    print_header "Frontend Setup (Node.js)"
    setup_frontend
    
    print_header "Setup Complete!"
    print_next_steps
}

# Backend setup function
setup_backend() {
    print_step "Setting up Python backend environment..."
    
    # Check if Python is available
    if ! command_exists python3; then
        print_error "Python3 is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    # Navigate to backend directory
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [[ ! -d "venv" ]]; then
        print_step "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Created virtual environment"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_step "Activating virtual environment..."
    source venv/bin/activate
    print_success "Activated virtual environment"
    
    # Upgrade pip, wheel, and setuptools
    print_step "Upgrading pip, wheel, and setuptools..."
    pip install --upgrade pip wheel setuptools
    print_success "Upgraded pip, wheel, and setuptools"
    
    # Install dependencies from requirements.txt
    print_step "Installing Python dependencies..."
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        print_success "Installed Python dependencies"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
    
    # Initialize database
    print_step "Initializing database..."
    python -c "from models.database import init_db; init_db()"
    print_success "Database initialized"
    
    # Deactivate virtual environment
    deactivate
    
    # Go back to project root
    cd ..
    
    print_success "Backend setup completed"
}

# Frontend setup function
setup_frontend() {
    print_step "Setting up React Native frontend environment..."
    
    # Check if Node.js is available
    if ! command_exists node; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Check if npm is available
    if ! command_exists npm; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    # Navigate to frontend directory
    cd frontend
    
    # Install dependencies from package.json
    print_step "Installing Node.js dependencies..."
    if [[ -f "package.json" ]]; then
        npm install
        print_success "Installed Node.js dependencies"
    else
        print_error "package.json not found"
        exit 1
    fi
    
    # Go back to project root
    cd ..
    
    print_success "Frontend setup completed"
}

# Print next steps
print_next_steps() {
    echo -e "\n${GREEN}🎉 Setup completed successfully!${NC}\n"
    
    echo -e "${BLUE}To run the backend:${NC}"
    echo -e "  cd backend"
    echo -e "  source venv/bin/activate"
    echo -e "  python app.py"
    echo -e ""
    
    echo -e "${BLUE}To run the frontend:${NC}"
    echo -e "  cd frontend"
    echo -e "  npm start"
    echo -e ""
    
    echo -e "${BLUE}To run tests:${NC}"
    echo -e "  cd backend"
    echo -e "  source venv/bin/activate"
    echo -e "  pytest"
    echo -e ""
    
    echo -e "${YELLOW}Note: Make sure to activate the virtual environment before running Python commands!${NC}"
}

# Handle script interruption
trap 'echo -e "\n${YELLOW}Setup interrupted by user${NC}"; exit 1' INT

# Run main function
main "$@"