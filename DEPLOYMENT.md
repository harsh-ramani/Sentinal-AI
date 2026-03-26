# 🛡️ Global Border AI - Deployment Guide

## Deployment on Streamlit Cloud

This guide covers deploying your Streamlit application to Streamlit Cloud, or other hosting platforms.

### Prerequisites
- Python 3.8 or higher
- All dependencies listed in `requirements.txt`
- Git repository (for Streamlit Cloud)

### Files Included

#### 1. **requirements.txt**
Contains all Python package dependencies with pinned versions for reproducibility:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `plotly` - Interactive visualizations
- `scikit-learn` - Machine learning models
- `opencv-python` - Computer vision library

#### 2. **.streamlit/config.toml**
Streamlit configuration file that sets:
- Color theme (dark mode with gradient colors)
- Toolbar settings
- Logger settings
- Font preferences

### Deployment Steps

#### Option 1: Streamlit Cloud (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Sign in with GitHub account

3. **Create a new app**
   - Click "New app"
   - Select your repository
   - Select branch: `main` (or your preferred branch)
   - Set main file path: `app.py`
   - Click "Deploy"

#### Option 2: Heroku Deployment

1. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create .env file** (optional)
   ```
   PYTHONUNBUFFERED=1
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

#### Option 3: Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Then build and run:
```bash
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
```

### Environment Variables (Optional)

For Streamlit Cloud, add secrets in `.streamlit/secrets.toml`:
```toml
# Example for API keys or credentials
api_key = "your-secret-key"
database_url = "your-database-url"
```

Note: Never commit `secrets.toml` to version control. Use Streamlit Cloud's secrets management instead.

### Local Testing

Before deployment, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Performance Optimization

1. **Cache data** using `@st.cache_data` decorator
2. **Minimize model loading** with `@st.cache_resource`
3. **Use `st.session_state`** for state management
4. **Lazy load resources** on demand

### Troubleshooting

#### Module Not Found Error
- Ensure all packages in `requirements.txt` are listed
- Run `pip install -r requirements.txt` locally first

#### Memory Issues
- Reduce model complexity or data size
- Use streaming for large files
- Implement pagination for datasets

#### Slow Performance
- Add caching decorators to expensive operations
- Profile your code with `streamlit run app.py --logger.level=debug`

### Version Updates

To update dependencies:
```bash
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
```

### Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud Deployment](https://docs.streamlit.io/streamlit-cloud)
- [GitHub Actions for CI/CD](https://github.com/features/actions)

---
**Last Updated:** March 2026
