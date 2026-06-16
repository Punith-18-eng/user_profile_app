#!/bin/bash
# Startup script for Text Classification Project
# Usage: ./start.sh [flask|streamlit|both|docker]

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✅ ${1}${NC}"
}

print_error() {
    echo -e "${RED}❌ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  ${1}${NC}"
}

# Function to check if model files exist
check_model_files() {
    if [[ ! -f "saved_models/text_classification_model.h5" ]]; then
        print_error "Model file not found: saved_models/text_classification_model.h5"
        echo "Please run the Jupyter notebook first to train and save the model."
        echo "Or restore the model from backup."
        return 1
    fi
    if [[ ! -f "saved_models/tokenizer.pickle" ]]; then
        print_error "Tokenizer file not found: saved_models/tokenizer.pickle"
        return 1
    fi
    if [[ ! -f "saved_models/config.pickle" ]]; then
        print_error "Config file not found: saved_models/config.pickle"
        return 1
    fi
    return 0
}

# Function to check dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        return 1
    fi
    print_success "Python 3 found: $(python3 --version)"
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed"
        return 1
    fi
    print_success "pip3 found"
    
    # Check virtual environment
    if [[ ! -d "venv" ]]; then
        print_warning "Virtual environment not found. Creating one..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
    
    # Check installed packages
    if ! python3 -c "import tensorflow" 2>/dev/null; then
        print_warning "TensorFlow not installed. Installing dependencies..."
        pip3 install -r requirements_deployment.txt
        print_success "Dependencies installed"
    else
        print_success "All required packages are installed"
    fi
    
    return 0
}

# Function to start Flask API
start_flask() {
    print_info "Starting Flask API..."
    
    if ! check_model_files; then
        return 1
    fi
    
    if ! check_dependencies; then
        return 1
    fi
    
    source venv/bin/activate
    print_success "Starting Flask API on http://localhost:5000"
    echo ""
    python3 flask_app.py
}

# Function to start Streamlit app
start_streamlit() {
    print_info "Starting Streamlit app..."
    
    if ! check_model_files; then
        return 1
    fi
    
    if ! check_dependencies; then
        return 1
    fi
    
    source venv/bin/activate
    print_success "Starting Streamlit app on http://localhost:8501"
    echo ""
    streamlit run streamlit_app.py
}

# Function to start both with Docker
start_docker() {
    print_info "Starting with Docker..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        echo "Please install Docker from https://www.docker.com"
        return 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        return 1
    fi
    
    print_success "Docker found"
    echo ""
    print_info "Building Docker image..."
    docker-compose build
    
    echo ""
    print_success "Starting containers..."
    docker-compose up -d
    
    echo ""
    print_success "Containers started successfully!"
    echo ""
    echo "Services available at:"
    echo "  🔌 Flask API: http://localhost:5000"
    echo "  🎨 Streamlit: http://localhost:8501"
    echo ""
    echo "View logs:"
    echo "  Flask:     docker-compose logs -f flask-api"
    echo "  Streamlit: docker-compose logs -f streamlit-app"
    echo ""
    echo "Stop containers:"
    echo "  docker-compose down"
}

# Function to start both locally
start_both() {
    print_info "Starting both Flask and Streamlit..."
    
    if ! check_dependencies; then
        return 1
    fi
    
    source venv/bin/activate
    
    # Start Flask in background
    print_success "Starting Flask API in background..."
    python3 flask_app.py &
    FLASK_PID=$!
    sleep 2
    
    # Start Streamlit
    print_success "Starting Streamlit app..."
    streamlit run streamlit_app.py
    
    # Cleanup
    trap "kill $FLASK_PID" EXIT
}

# Function to show help
show_help() {
    echo ""
    echo "Text Classification Project - Startup Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  flask       Start Flask REST API only"
    echo "  streamlit   Start Streamlit web app only"
    echo "  both        Start both Flask and Streamlit locally"
    echo "  docker      Start both using Docker Compose"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 flask                    # Start Flask API"
    echo "  $0 streamlit               # Start Streamlit web app"
    echo "  $0 docker                  # Start with Docker"
    echo ""
    echo "Default (no arguments): Show this help message"
    echo ""
}

# Main script
main() {
    clear
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║      Text Classification with TensorFlow - Startup Script      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    case "${1:-help}" in
        flask)
            start_flask
            ;;
        streamlit)
            start_streamlit
            ;;
        both)
            start_both
            ;;
        docker)
            start_docker
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
