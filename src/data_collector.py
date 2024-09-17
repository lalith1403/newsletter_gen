# src/data_collector.py

import os
import json
import requests
from datetime import datetime
from config import GITHUB_TOKEN

class GitHubDataCollector:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.api_base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'github_data')
        os.makedirs(self.data_dir, exist_ok=True)

    def get_repo_info(self):
        owner, repo = self.repo_url.split("/")[-2:]
        url = f"{self.api_base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_recent_commits(self, days=7):
        owner, repo = self.repo_url.split("/")[-2:]
        url = f"{self.api_base_url}/repos/{owner}/{repo}/commits"
        params = {"since": f"{days}d"}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_recent_issues(self, days=7):
        owner, repo = self.repo_url.split("/")[-2:]
        url = f"{self.api_base_url}/repos/{owner}/{repo}/issues"
        params = {"state": "all", "since": f"{days}d"}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def collect_data(self):
        data = {
            "repo_info": self.get_repo_info(),
            "recent_commits": self.get_recent_commits(),
            "recent_issues": self.get_recent_issues()
        }
        self.save_data(data)
        return data

    def save_data(self, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        owner, repo = self.repo_url.split("/")[-2:]
        filename = f"{owner}_{repo}_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filepath}")

    def load_latest_data(self):
        files = os.listdir(self.data_dir)
        if not files:
            return None
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.data_dir, f)))
        filepath = os.path.join(self.data_dir, latest_file)
        with open(filepath, 'r') as f:
            return json.load(f)