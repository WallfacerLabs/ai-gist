# Tests for vaults.fyi Documentation

This directory contains comprehensive tests to verify that all code examples, commands, and instructions in the vaults.fyi API documentation (`claude.md`) are correct and working.

## Overview

The tests validate:
- ✅ **SDK Installation**: Both Python and JavaScript SDK installation commands
- ✅ **Import Statements**: All documented import patterns and syntax
- ✅ **Code Examples**: Every code example in the documentation
- ✅ **Virtual Environment Setup**: Python virtual environment commands
- ✅ **Best Practices**: Documented development workflows
- ✅ **API Method Signatures**: All endpoint examples and parameter structures

## Test Structure

```
tests/
├── README.md           # This file
├── run-all-tests.sh   # Main test runner script
├── js/                # JavaScript tests
│   ├── package.json
│   ├── test-runner.js
│   ├── test-imports.js
│   └── test-examples.js
└── python/            # Python tests
    ├── requirements.txt
    ├── test_runner.py
    ├── test_imports.py
    └── test_venv_setup.py
```

## Running Tests

### Run All Tests
```bash
# From the tests directory
./run-all-tests.sh
```

### Run JavaScript Tests Only
```bash
cd tests/js
npm install
npm test
```

### Run Python Tests Only
```bash
cd tests/python

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_runner.py
```

## What Each Test Does

### JavaScript Tests (`tests/js/`)

#### `test-imports.js`
- ✅ Tests ES Module import: `import pkg from '@vaultsfyi/sdk'`
- ✅ Tests CommonJS import: `require('@vaultsfyi/sdk')`
- ✅ Tests TypeScript-style import patterns
- ✅ Validates all SDK methods exist
- ✅ Checks parameter structure validation

#### `test-examples.js`
- ✅ Tests all JavaScript code examples from documentation
- ✅ Validates `getBenchmarks()` example
- ✅ Validates `getAllVaults()` credit-efficient filtering
- ✅ Validates `getActions()` transaction generation
- ✅ Tests best practices examples
- ✅ Validates Common Patterns section examples

### Python Tests (`tests/python/`)

#### `test_imports.py`
- ✅ Tests basic SDK import: `from vaultsfyi import VaultsSdk`
- ✅ Tests SDK initialization examples
- ✅ Validates all documented SDK methods exist
- ✅ Tests exception class imports
- ✅ Validates all code examples from documentation
- ✅ Tests network validation functions
- ✅ Tests correct best yields function (using `get_deposit_options`)

#### `test_venv_setup.py`
- ✅ Tests `python -m venv venv` command
- ✅ Validates virtual environment structure
- ✅ Tests activation script existence
- ✅ Tests pip install in virtual environment
- ✅ Tests `pip freeze > requirements.txt` workflow
- ✅ Validates .gitignore patterns
- ✅ Tests recommended project structure

## Test Requirements

### JavaScript Requirements
- Node.js 16+
- npm
- `@vaultsfyi/sdk` package

### Python Requirements
- Python 3.7+
- `vaultsfyi` package
- `pytest` (optional, for extended testing)

## Environment Variables

Some tests may use environment variables:
- `VAULTS_FYI_API_KEY`: For testing SDK initialization patterns

Note: Tests do not make actual API calls. They validate code structure, imports, and examples without requiring a valid API key.

## Continuous Integration

These tests are designed to be run in CI/CD pipelines to ensure documentation accuracy:

```yaml
# Example GitHub Actions workflow
name: Documentation Tests
on: [push, pull_request]
jobs:
  test-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Run documentation tests
        run: cd tests && ./run-all-tests.sh
```

## Contributing

When updating the documentation (`claude.md`):

1. **Add corresponding tests** for any new code examples
2. **Update existing tests** if API signatures change
3. **Run all tests** before committing changes
4. **Update test descriptions** to match new functionality

### Adding New Tests

#### For JavaScript Examples:
Add test cases to `tests/js/test-examples.js`:

```javascript
test('New feature example', async () => {
    const pkg = await import('@vaultsfyi/sdk');
    const { VaultsSdk } = pkg;
    const client = new VaultsSdk({ apiKey: 'test_key' });
    
    // Test your new example here
});
```

#### For Python Examples:
Add test methods to `tests/python/test_imports.py`:

```python
def test_new_feature_example(self):
    """Test new feature example from documentation"""
    from vaultsfyi import VaultsSdk
    client = VaultsSdk(api_key="test_key")
    
    # Test your new example here
```

## Troubleshooting

### Common Issues

**"Module not found" errors:**
- Ensure you've installed dependencies: `npm install` or `pip install -r requirements.txt`
- For Python: Make sure you're in a virtual environment

**"API key" related errors:**
- Tests don't make real API calls, so errors about invalid keys are expected
- Tests validate structure and imports, not API responses

**Virtual environment tests failing:**
- Some tests create temporary virtual environments
- Ensure you have sufficient disk space and permissions

### Test Debugging

Enable verbose output:
```bash
# JavaScript
cd tests/js && npm test -- --verbose

# Python  
cd tests/python && python test_runner.py -v
```

## Success Criteria

All tests should pass when:
- ✅ All code examples in `claude.md` are syntactically correct
- ✅ All import statements work with current SDK versions
- ✅ All documented commands execute successfully
- ✅ Virtual environment setup follows best practices
- ✅ SDK methods and parameters match documentation
- ✅ No hardcoded values that should be dynamic

This ensures the documentation is always accurate and actionable for developers.