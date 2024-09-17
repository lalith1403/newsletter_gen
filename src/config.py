# src/config.py

import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

REPO_URL = ""
RECIPIENTS = []
FREQUENCY = "weekly"
