#!/bin/bash

# RTX 3090 Quick Test - Main Script
# Usage: bash quick_test.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_WARNING=0

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║           RTX 3090 QUICK TEST - SHOP VERSION              ║
║                   Test Time: ~12 minutes                  ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check requirements
echo "Checking requirements..."

if ! command -v nvidia-smi &> /dev/null; then
    echo -e "${RED}❌ nvidia-smi not found. Install NVIDIA drivers first.${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found.${NC}"
    exit 1
fi

# Check PyTorch
if ! python3 -c "import torch" &> /dev/null; then
    echo -e "${RED}❌ PyTorch not found.${NC}"
    echo "Install: pip install torch --index-url https://download.pytorch.org/whl/cu124"
    exit 1
fi

if ! python3 -c "import torch; assert torch.cuda.is_available()" &> /dev/null; then
    echo -e "${RED}❌ CUDA not available in PyTorch.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All requirements met${NC}\n"

# Start tests
echo "═══════════════════════════════════════════════════════════"
echo "                    STARTING TESTS"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Test 1: GPU Info
echo -e "${BLUE}[1/4]${NC} GPU Information Check..."
if python3 tests/gpu_info.py; then
    echo -e "${GREEN}✅ GPU Info: PASS${NC}\n"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}❌ GPU Info: FAIL${NC}\n"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: VRAM Test (CRITICAL)
echo -e "${BLUE}[2/4]${NC} VRAM Stress Test (5 minutes) - CRITICAL..."
echo "This is the most important test. Any errors = DO NOT BUY!"
if python3 tests/vram_test.py --duration 5 --size 20; then
    echo -e "${GREEN}✅ VRAM Test: PASS (0 errors)${NC}\n"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}❌ VRAM Test: FAIL - DO NOT BUY THIS GPU!${NC}\n"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Thermal Test
echo -e "${BLUE}[3/4]${NC} Thermal Stress Test (3 minutes)..."
set +e  # Temporarily disable exit on error to capture exit code
python3 tests/thermal_test.py --duration 3
EXIT_CODE=$?
set -e  # Re-enable exit on error

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Thermal Test: PASS${NC}\n"
    TESTS_PASSED=$((TESTS_PASSED + 1))
elif [ $EXIT_CODE -eq 2 ]; then
    echo -e "${YELLOW}⚠️  Thermal Test: WARNING (high temps but acceptable)${NC}\n"
    TESTS_WARNING=$((TESTS_WARNING + 1))
else
    echo -e "${RED}❌ Thermal Test: FAIL${NC}\n"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 4: Performance Test
echo -e "${BLUE}[4/4]${NC} Performance Benchmark (2 minutes)..."
set +e  # Temporarily disable exit on error to capture exit code
python3 tests/performance_test.py
EXIT_CODE=$?
set -e  # Re-enable exit on error

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Performance Test: PASS${NC}\n"
    TESTS_PASSED=$((TESTS_PASSED + 1))
elif [ $EXIT_CODE -eq 2 ]; then
    echo -e "${YELLOW}⚠️  Performance Test: WARNING (below expected but acceptable)${NC}\n"
    TESTS_WARNING=$((TESTS_WARNING + 1))
else
    echo -e "${RED}❌ Performance Test: FAIL${NC}\n"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "                      TEST SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "Tests Passed:  ${GREEN}${TESTS_PASSED}/4${NC}"
echo -e "Tests Warning: ${YELLOW}${TESTS_WARNING}/4${NC}"
echo -e "Tests Failed:  ${RED}${TESTS_FAILED}/4${NC}"
echo ""

# Final decision
if [ $TESTS_FAILED -eq 0 ] && [ $TESTS_WARNING -eq 0 ]; then
    echo "═══════════════════════════════════════════════════════════"
    echo -e "${GREEN}✅ OVERALL RESULT: PASS${NC}"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "✅ This GPU is in good condition for AI/ML workloads"
    echo "✅ Safe to buy at fair price (~22-23.5M VND)"
    echo ""
    exit 0
elif [ $TESTS_FAILED -eq 0 ]; then
    echo "═══════════════════════════════════════════════════════════"
    echo -e "${YELLOW}⚠️  OVERALL RESULT: ACCEPTABLE WITH WARNINGS${NC}"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "⚠️  GPU has minor issues but may be acceptable"
    echo "⚠️  Negotiate price down 1-2M VND"
    echo "⚠️  Request longer warranty (6+ months)"
    echo ""
    exit 0
else
    echo "═══════════════════════════════════════════════════════════"
    echo -e "${RED}❌ OVERALL RESULT: FAIL${NC}"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "❌ DO NOT BUY THIS GPU"
    echo ""
    exit 1
fi