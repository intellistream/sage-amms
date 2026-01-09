#!/bin/bash
# Build script for SAGE-AMMS

set -e

echo "=== Building SAGE-AMMS ==="
echo ""

# Parse arguments
BUILD_TYPE="cpu"
VERBOSE=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --cuda)
            BUILD_TYPE="cuda"
            shift
            ;;
        --verbose|-v)
            VERBOSE=1
            shift
            ;;
        --help|-h)
            echo "Usage: ./build.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --cuda         Build with CUDA support"
            echo "  --verbose, -v  Verbose output"
            echo "  --help, -h     Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.so" -delete 2>/dev/null || true

echo "✓ Cleaned"
echo ""

# Set build environment
if [ "$BUILD_TYPE" = "cuda" ]; then
    echo "Building with CUDA support..."
    export AMMS_ENABLE_CUDA=1
    if [ -z "$CUDA_HOME" ]; then
        export CUDA_HOME=/usr/local/cuda
    fi
    echo "CUDA_HOME: $CUDA_HOME"
else
    echo "Building CPU-only version..."
    export AMMS_ENABLE_CUDA=0
fi

# Build
echo ""
echo "Building wheel..."
if [ $VERBOSE -eq 1 ]; then
    python -m build --wheel -v
else
    python -m build --wheel
fi

echo ""
echo "✓ Build complete!"
echo ""
echo "Wheel location:"
ls -lh dist/*.whl

echo ""
echo "To install:"
echo "  pip install dist/*.whl"
