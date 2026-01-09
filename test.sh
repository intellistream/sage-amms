#!/bin/bash
# Quick test script for SAGE-AMMS

set -e

echo "=== SAGE-AMMS Quick Test ==="
echo ""

echo "1. Testing imports..."
python -c "import sage.libs.amms; print(f'✓ Package version: {sage.libs.amms.__version__}')"

echo ""
echo "2. Testing package structure..."
python -c "import sage.libs.amms.wrappers; print('✓ Wrappers module exists')"

echo ""
echo "3. Testing PyAMM wrapper..."
python -c "
try:
    from sage.libs.amms.wrappers import pyamm
    print('✓ PyAMM wrapper imported')
    if hasattr(pyamm, '_has_extension'):
        if pyamm._has_extension:
            print('✓ C++ extension available')
        else:
            print('⚠ C++ extension not built (this is okay for interface-only tests)')
except ImportError as e:
    print(f'⚠ PyAMM C++ extension not available: {e}')
    print('  This is expected if package is not fully built yet')
" || true

echo ""
echo "4. Running unit tests..."
pytest tests/ -v --tb=short

echo ""
echo "=== All Tests Passed! ==="
