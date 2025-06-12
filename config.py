"""Configuration and constants for the Crew AI project."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# LLM Configuration
DEFAULT_LLM = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7

# Agent Configuration
DEFAULT_VERBOSE = True
DEFAULT_ALLOW_DELEGATION = False

# Task Configuration
DEFAULT_MAX_ITERATIONS = 3

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate required environment variables
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
