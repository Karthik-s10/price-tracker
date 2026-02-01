#!/bin/bash

# Install the package in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p .streamlit

# Create a default config.toml if it doesn't exist
if [ ! -f .streamlit/config.toml ]; then
    cat > .streamlit/config.toml << EOL
[server]
headless = true
port = $PORT
enableCORS = false

[theme]
base = "dark"
primaryColor = "#7e57c2"
backgroundColor = "#1e1e1e"
secondaryBackgroundColor = "#2d2d2d"
textColor = "#fafafa"
font = "sans serif"
EOL
fi

# Run the Streamlit app
streamlit run streamlit_app.py
