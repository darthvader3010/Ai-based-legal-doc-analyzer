#!/bin/bash

# Setup script for AI-Based Legal Document Analyzer
# This script will set up the environment and install dependencies

set -e  # Exit on error

echo "=========================================="
echo "AI-Based Legal Document Analyzer"
echo "Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

# Check if Python version is 3.8 or higher
REQUIRED_VERSION="3.8"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python 3.8 or higher is required. You have Python $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python version is compatible"
echo ""

# Check if pip is installed
echo "Checking for pip..."
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed. Please install pip."
    exit 1
fi

echo "✓ pip is installed"
echo ""

# Ask user if they want to create a virtual environment
read -p "Do you want to create a virtual environment? (recommended) [Y/n]: " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "✓ Virtual environment created"
    echo ""
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "✓ Virtual environment activated"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""

pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Create uploads directory
echo "Creating uploads directory..."
mkdir -p uploads
echo "✓ Uploads directory created"
echo ""

# Run tests to verify installation
echo "Running tests to verify installation..."
python -m pytest test_analyzer.py -v --tb=short

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "You can now use the analyzer in three ways:"
    echo ""
    echo "1. Web Application:"
    echo "   python app.py"
    echo "   Then visit: http://localhost:5000"
    echo ""
    echo "2. Command Line:"
    echo "   python cli.py analyze document.pdf"
    echo "   python cli.py search document.pdf --keywords 'liability,warranty'"
    echo ""
    echo "3. Python API:"
    echo "   See example_usage.py for code examples"
    echo ""
    echo "For more information, see README.md"
    echo ""
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "Note: To activate the virtual environment in future sessions, run:"
        echo "   source venv/bin/activate"
        echo ""
    fi
else
    echo ""
    echo "=========================================="
    echo "✗ Setup failed - tests did not pass"
    echo "=========================================="
    echo ""
    echo "Please check the error messages above and try again."
    exit 1
fi
