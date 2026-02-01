from setuptools import setup, find_packages

setup(
    name="price-tracker",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["streamlit_app"],
    install_requires=[
        "streamlit>=1.28.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.0.0",
        "plotly>=5.17.0",
        "lxml>=4.9.0"
    ],
)
