#!/bin/bash

# Main test runner for vaults.fyi documentation tests
# Runs both JavaScript and Python tests to verify all documentation examples

set -e  # Exit on any error

echo "🚀 Running All Tests for vaults.fyi Documentation"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track test results
TOTAL_SUITES=0
PASSED_SUITES=0

# Function to run a test suite
run_test_suite() {
    local suite_name="$1"
    local test_command="$2"
    local test_dir="$3"
    
    echo -e "${BLUE}🧪 Running $suite_name Tests...${NC}"
    echo "----------------------------------------"
    
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    
    # Change to test directory if specified
    if [ -n "$test_dir" ]; then
        cd "$test_dir"
    fi
    
    # Run the test command
    if eval "$test_command"; then
        echo -e "${GREEN}✅ $suite_name tests passed${NC}"
        PASSED_SUITES=$((PASSED_SUITES + 1))
    else
        echo -e "${RED}❌ $suite_name tests failed${NC}"
        echo ""
        echo -e "${YELLOW}⚠️  Continuing with remaining tests...${NC}"
    fi
    
    echo ""
    
    # Return to original directory
    if [ -n "$test_dir" ]; then
        cd - > /dev/null
    fi
}

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📋 Test Plan:"
echo "   1. JavaScript SDK Tests (imports, examples)"
echo "   2. Python SDK Tests (imports, examples, virtual environment)"
echo ""

# JavaScript Tests
echo -e "${BLUE}📦 Checking JavaScript Environment...${NC}"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 16+ to run JavaScript tests"
    echo "Visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION detected"

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

echo "✅ npm detected"
echo ""

# Install JavaScript dependencies
echo -e "${BLUE}📦 Installing JavaScript dependencies...${NC}"
cd js
if npm install; then
    echo -e "${GREEN}✅ JavaScript dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install JavaScript dependencies${NC}"
    exit 1
fi
cd ..
echo ""

# Run JavaScript tests
run_test_suite "JavaScript SDK" "npm test" "js"

# Python Tests
echo -e "${BLUE}🐍 Checking Python Environment...${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed${NC}"
    echo "Please install Python 3.7+ to run Python tests"
    exit 1
fi

# Use python3 if available, otherwise python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo "✅ $PYTHON_VERSION detected"

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Running in virtual environment: $VIRTUAL_ENV"
    VENV_STATUS="active"
else
    echo -e "${YELLOW}⚠️  Not running in a virtual environment${NC}"
    echo "   Recommendation: python -m venv venv && source venv/bin/activate"
    VENV_STATUS="none"
fi
echo ""

# Handle Python dependencies and virtual environment
echo -e "${BLUE}📦 Setting up Python environment...${NC}"
cd python

# Check if we need to create a virtual environment for testing
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Creating temporary virtual environment for testing..."
    
    # Create a temporary venv for testing
    if $PYTHON_CMD -m venv test_venv; then
        echo "✅ Test virtual environment created"
        
        # Activate the virtual environment
        source test_venv/bin/activate
        echo "✅ Virtual environment activated"
        
        # Update Python command to use venv python
        PYTHON_CMD="python"
        USING_TEST_VENV=true
    else
        echo -e "${YELLOW}⚠️  Could not create virtual environment${NC}"
        echo "   Will attempt to install with system Python"
        USING_TEST_VENV=false
    fi
else
    USING_TEST_VENV=false
fi

# Try to install dependencies
echo "Installing Python dependencies..."
if $PYTHON_CMD -m pip install -r requirements.txt; then
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  Some Python dependencies may not be available${NC}"
    echo "   This is expected if SDKs are not public yet"
    echo "   Tests will verify import structure and examples anyway"
fi

cd ..
echo ""

# Run Python tests
run_test_suite "Python SDK" "$PYTHON_CMD test_runner.py" "python"

# Cleanup test virtual environment if we created one
if [[ "$USING_TEST_VENV" == "true" ]]; then
    echo -e "${BLUE}🧹 Cleaning up test virtual environment...${NC}"
    cd python
    deactivate 2>/dev/null || true
    rm -rf test_venv
    echo "✅ Test virtual environment cleaned up"
    cd ..
fi

# Final Results
echo "========================================================"
echo -e "${BLUE}📊 Final Test Results${NC}"
echo "========================================================"
echo "Test suites passed: $PASSED_SUITES/$TOTAL_SUITES"
echo ""

if [ $PASSED_SUITES -eq $TOTAL_SUITES ]; then
    echo -e "${GREEN}🎉 All test suites passed!${NC}"
    echo -e "${GREEN}✅ Documentation examples are working correctly${NC}"
    
    if [ "$VENV_STATUS" = "none" ]; then
        echo ""
        echo -e "${YELLOW}💡 Tip: Consider using virtual environments for Python development${NC}"
        echo "   Commands: python -m venv venv && source venv/bin/activate"
    fi
    
    exit 0
else
    echo -e "${RED}💥 Some test suites failed${NC}"
    echo -e "${RED}❌ Documentation may need updates${NC}"
    echo ""
    echo "Common fixes:"
    echo "  • Check SDK installation: npm install @vaultsfyi/sdk"
    echo "  • Check Python SDK: pip install vaultsfyi"
    echo "  • Verify code examples in claude.md"
    echo "  • Check import statements and method signatures"
    exit 1
fi