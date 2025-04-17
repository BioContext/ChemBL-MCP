# Contributing to ChemBL-MCP

Thank you for your interest in contributing to ChemBL-MCP! This document outlines the process for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improving the ChemBL-MCP server:

1. Check if the issue has already been reported in the [Issues](https://github.com/BioContext/ChemBL-MCP/issues) section.
2. If not, create a new issue, providing as much detail as possible:
   - A clear description of the issue or suggestion
   - Steps to reproduce (for bugs)
   - Expected behavior
   - Actual behavior
   - Your environment (OS, Python version, etc.)

### Contributing Code

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add or update tests as necessary
5. Ensure all tests pass
6. Submit a pull request

### Pull Request Process

1. Update the README.md or documentation with details of changes, if applicable
2. Ensure your code follows the project's coding style
3. The PR should work on the main branch
4. Link any relevant issues in your PR description

## Development Environment

```bash
# Clone the repository
git clone https://github.com/BioContext/ChemBL-MCP.git
cd ChemBL-MCP

# Create a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Code Style

This project follows PEP 8 style guidelines. Please ensure your code adheres to these standards.

## Testing

Please include tests for any new features or bug fixes. All tests should pass before submitting a pull request.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE). 