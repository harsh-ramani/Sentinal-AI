# Development Setup Guide

## Initial Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/global-border-ai.git
cd global-border-ai
```

### 2. Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .  # Install in development mode (optional, if using setup.py)
```

### 4. Configuration

#### Local Development Secrets
Create `.streamlit/secrets.toml` from the template:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit the file with your local credentials (this file is gitignored, won't be committed).

#### Environment Variables
```bash
# Optional: Create .env file with development settings
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=localhost
```

### 5. Run Application
```bash
streamlit run app.py
```

The app will start at: `http://localhost:8501`

## Development Workflow

### Before Each Session
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Update dependencies (optional)
pip install --upgrade -r requirements.txt
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test locally
streamlit run app.py

# Add and commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin feature/your-feature-name
```

### Testing
```bash
# Run the app in test mode
streamlit run app.py --logger.level=debug

# Check for syntax errors
python -m py_compile app.py

# Run any unit tests (if added)
python -m pytest tests/
```

## Dependency Management

### Adding New Dependencies
```bash
# Install new package
pip install new-package

# Update requirements.txt
pip freeze > requirements.txt
```

### Updating Existing Dependencies
```bash
# Update specific package
pip install --upgrade package-name

# Update all packages
pip install --upgrade -r requirements.txt

# Update requirements file
pip freeze > requirements.txt
```

### Checking Outdated Packages
```bash
pip list --outdated
```

## Troubleshooting Development

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip show package-name
```

### Port Already in Use
```bash
# Change port
streamlit run app.py --server.port=8502
```

### Cache Issues
```bash
# Clear Streamlit cache
streamlit cache clear

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv  # or rmdir venv on Windows

# Create fresh environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

## IDE Setup

### VS Code
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

### PyCharm
1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add...
3. Select "Existing Environment"
4. Navigate to `venv/bin/python` (or `venv\Scripts\python.exe` on Windows)

## Code Standards

### Style Guide
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes

### Formatting
```bash
# Format code with black
pip install black
black app.py

# Sort imports with isort
pip install isort
isort app.py
```

### Linting
```bash
# Check code with pylint
pip install pylint
pylint app.py

# Check code with flake8
pip install flake8
flake8 app.py
```

## Performance Profiling

```bash
# Run with debug logging
streamlit run app.py --logger.level=debug

# Profile Python execution
pip install line_profiler
kernprof -l -v app.py
```

## Useful Streamlit Commands

```bash
# Show version
streamlit --version

# Show help
streamlit run --help

# Run in headless mode (no browser)
streamlit run app.py --server.headless=true

# Run with specific config
streamlit run app.py --config.toml=.streamlit/config.toml
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Python Packaging Guide](https://packaging.python.org)
- [Git Documentation](https://git-scm.com/doc)
- [Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)

---

**Last Updated:** March 2026
