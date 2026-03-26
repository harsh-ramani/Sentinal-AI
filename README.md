# 🛡️ Global Border AI

Advanced AI-powered Streamlit application for border security analysis and threat detection.

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/global-border-ai.git
   cd global-border-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8501`

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions including:
- Streamlit Cloud deployment
- Heroku deployment
- Docker containerization
- Environment configuration

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup configuration
├── DEPLOYMENT.md              # Deployment guide
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── Procfile                   # Heroku deployment configuration
├── .python-version            # Python version specification
├── .gitignore                 # Git ignore patterns
└── .streamlit/
    ├── config.toml            # Streamlit configuration
    └── secrets.toml.example   # Secrets template (NEVER commit actual secrets)
```

## Features

- 🎯 Real-time threat analysis
- 📊 Interactive data visualizations
- 🤖 Machine learning-powered predictions
- 💻 User-friendly web interface
- 🔐 Secure credential management

## Requirements

- Python 3.8+
- All packages listed in `requirements.txt`

## Technologies Used

- **Streamlit** - Web framework
- **Pandas & NumPy** - Data processing
- **Plotly** - Interactive visualizations
- **scikit-learn** - Machine learning
- **OpenCV** - Computer vision

## Environment Variables

Optional environment variables for configuration:
```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

For sensitive data, use `.streamlit/secrets.toml` (see `.streamlit/secrets.toml.example`)

## Performance Tips

- Use `@st.cache_data` for expensive computations
- Use `@st.cache_resource` for models and connections
- Implement pagination for large datasets
- Monitor memory usage for large models

## Troubleshooting

### Module Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Memory Issues
- Reduce batch sizes
- Stream large data
- Use data partitioning

### Slow Performance
- Enable caching for expensive operations
- Profile with: `streamlit run app.py --logger.level=debug`
- Check resource utilization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions and support:
- Email: your.email@example.com
- GitHub Issues: [Your Repository Issues](https://github.com/yourusername/global-border-ai/issues)

## Acknowledgments

- Streamlit team for the amazing web framework
- Open-source maintainers of pandas, numpy, plotly, and scikit-learn
- Community contributors

---

**Last Updated:** March 2026  
**Version:** 1.0.0
