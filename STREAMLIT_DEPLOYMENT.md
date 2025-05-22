# Deploying the Paint by Numbers Generator on Streamlit

This guide provides instructions for deploying the Paint by Numbers Generator application on Streamlit.

## Local Deployment

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app locally**:
   ```bash
   streamlit run app.py
   ```

3. **Access the app** in your web browser at `http://localhost:8501`

## Deploying to Streamlit Cloud

Streamlit Cloud is a free hosting service for Streamlit apps. Here's how to deploy your app:

1. **Create a GitHub repository** with your code:
   - Push your code to a GitHub repository
   - Make sure the repository includes:
     - `app.py`
     - `requirements.txt`
     - Any example images or assets needed

2. **Sign up for Streamlit Cloud**:
   - Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account

3. **Deploy your app**:
   - Click "New app"
   - Select your repository, branch, and the `app.py` file
   - Click "Deploy"

4. **Access your deployed app** at the URL provided by Streamlit Cloud

## Deploying to Heroku

Heroku is another popular platform for deploying web applications:

1. **Create a `Procfile`** in your project root with the following content:
   ```
   web: streamlit run app.py --server.port $PORT
   ```

2. **Create a `runtime.txt`** file with your Python version:
   ```
   python-3.9.13
   ```

3. **Install the Heroku CLI** and log in:
   ```bash
   heroku login
   ```

4. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```

5. **Push your code to Heroku**:
   ```bash
   git push heroku main
   ```

6. **Open your app**:
   ```bash
   heroku open
   ```

## Important Notes for Production Deployment

1. **Processing Large Images**: The current implementation simulates image processing. For a production deployment, you'll need to:
   - Compile the CLI version of the Paint by Numbers Generator
   - Integrate it with the Streamlit app to process images
   - Consider adding limits on image size to prevent server overload

2. **Temporary Files**: The app creates temporary files for processing. In a production environment:
   - Implement proper cleanup of temporary files
   - Consider using cloud storage for larger files

3. **Security Considerations**:
   - Validate all user inputs
   - Implement rate limiting to prevent abuse
   - Consider adding authentication if needed

4. **Performance Optimization**:
   - For high-traffic sites, consider caching results
   - Optimize image processing for better performance
   - Consider using a queue system for processing large images

## Customization

You can customize the app by:

1. **Changing the UI**: Modify the Streamlit components in `app.py`
2. **Adding features**: Implement additional functionality like:
   - More output formats
   - Advanced color selection
   - User accounts to save results
   - Batch processing

3. **Styling**: Customize the appearance using Streamlit's theming options:
   ```python
   st.set_page_config(
       page_title="Paint by Numbers Generator",
       page_icon="🎨",
       layout="wide",
       initial_sidebar_state="expanded",
       menu_items={
           'Get Help': 'https://github.com/yourusername/your-repo',
           'Report a bug': 'https://github.com/yourusername/your-repo/issues',
           'About': 'Paint by Numbers Generator - Convert images to paint-by-numbers style'
       }
   )
   ```
