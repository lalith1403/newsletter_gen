# src/data_collector.py

import requests
from config import GITHUB_TOKEN

class GitHubDataCollector:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.api_base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    def get_repo_info(self):
        owner, repo = self.repo_url.split("/")[-2:]
        url = f"{self.api_base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_recent_csommits(self, days=7):
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
        return {
            "repo_info": self.get_repo_info(),
            "recent_commits": self.get_recent_commits(),
            "recent_issues": self.get_recent_issues()
        }
