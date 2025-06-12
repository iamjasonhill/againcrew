from setuptools import setup, find_packages

setup(
    name="crew-ai-research-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crewai>=0.11.0",
        "streamlit>=1.23.0",
        "python-dotenv>=1.0.0",
        "rich>=13.0.0",
        "matplotlib>=3.7.0",
        "chromadb>=0.4.18,<0.5.0",
        "sentence-transformers>=2.2.2",
        "pypdf>=3.0.0",
        "pydantic>=2.0.0",
        "pytest>=7.0.0"
    ],
    python_requires=">=3.8",
)
