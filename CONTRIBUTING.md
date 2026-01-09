# Contributing to SAGE-AMMS

Thank you for your interest in contributing to SAGE-AMMS! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sage-amms.git
   cd sage-amms
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/intellistream/sage-amms.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- CMake 3.14 or higher
- C++14 compatible compiler
- PyTorch 2.0.0 or higher
- 64GB+ RAM recommended

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Optional: CUDA Development

```bash
# Install CUDA toolkit first, then:
AMMS_ENABLE_CUDA=1 pip install -e ".[dev,cuda]"
```

## Making Changes

### Branch Naming

- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`
- Performance: `perf/description`

Example:
```bash
git checkout -b feature/add-new-algorithm
```

### Commit Messages

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance

Example:
```
feat(algorithms): add new sketching algorithm

Implement the MinHash algorithm for approximate matrix multiplication.
Includes C++ implementation and Python bindings.

Closes #123
```

## Submitting Changes

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

3. **Check code style**:
   ```bash
   black sage/ tests/
   ruff check sage/ tests/
   ```

4. **Type checking** (optional but recommended):
   ```bash
   mypy sage/libs/amms/
   ```

### Creating Pull Request

1. Push to your fork:
   ```bash
   git push origin feature/your-feature
   ```

2. Go to GitHub and create a Pull Request

3. Fill in the PR template:
   - Description of changes
   - Related issues
   - Testing performed
   - Documentation updates

4. Wait for CI checks to pass

5. Respond to review comments

## Coding Standards

### Python Code

- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 100 characters
- Use Black for formatting
- Use Ruff for linting

```python
def multiply(matrix_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray:
    """Perform approximate matrix multiplication.
    
    Args:
        matrix_a: First input matrix (M x K).
        matrix_b: Second input matrix (K x N).
        
    Returns:
        Approximate result of matrix_a @ matrix_b.
    """
    pass
```

### C++ Code

- Follow Google C++ Style Guide
- Use C++14 features
- Include proper documentation
- Use meaningful variable names

```cpp
/**
 * @brief Perform sketching operation
 * 
 * @param input Input matrix
 * @param sketch_size Size of the sketch
 * @return Sketched matrix
 */
MatrixType sketch(const MatrixType& input, size_t sketch_size);
```

### Documentation

- Use NumPy-style docstrings for Python
- Use Doxygen-style comments for C++
- Include examples in docstrings
- Update README.md if adding features

## Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_interface.py -v

# With coverage
pytest tests/ --cov=sage.libs.amms --cov-report=html
```

### Writing Tests

Place tests in the `tests/` directory:

```python
# tests/test_my_feature.py
import pytest
from sage.libs.amms import create

def test_new_algorithm():
    """Test the new algorithm."""
    amm = create("newalgo", param=1)
    result = amm.multiply(matrix_a, matrix_b)
    assert result.shape == expected_shape
```

### Test Requirements

- Write tests for new features
- Maintain test coverage above 80%
- Include edge cases and error conditions
- Test both Python and C++ components

## Algorithm Implementation Guide

### Adding a New Algorithm

1. **C++ Implementation**:
   ```cpp
   // sage/libs/amms/implementations/include/CPPAlgos/NewAlgo.h
   class NewAlgoCPPAlgo : public AbstractCPPAlgo {
   public:
       void build(const MatrixType& matrix) override;
       MatrixType multiply(const MatrixType& a, const MatrixType& b) override;
   };
   ```

2. **Python Bindings**:
   ```cpp
   // In PyAMM.cpp
   py::class_<NewAlgoCPPAlgo>(m, "NewAlgo")
       .def(py::init<>())
       .def("build", &NewAlgoCPPAlgo::build)
       .def("multiply", &NewAlgoCPPAlgo::multiply);
   ```

3. **Python Wrapper**:
   ```python
   # sage/libs/amms/wrappers/pyamm.py
   # The C++ class is automatically exposed
   ```

4. **Tests**:
   ```python
   # tests/test_newalgo.py
   def test_newalgo():
       from sage.libs.amms.wrappers.pyamm import NewAlgo
       algo = NewAlgo()
       # Test implementation
   ```

5. **Documentation**:
   - Add to README.md algorithm list
   - Include paper references
   - Add usage examples

## Performance Considerations

- Profile before optimizing
- Use appropriate data structures
- Consider memory usage
- Benchmark against baselines
- Document performance characteristics

## Questions?

- Open an issue for bugs
- Start a discussion for questions
- Contact maintainers: shuhao_zhang@hust.edu.cn

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
