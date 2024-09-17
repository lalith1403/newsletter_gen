# src/data_collector.py

import os
import json
import requests
from datetime import datetime, timedelta
from config import GITHUB_TOKEN
from github import Github

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

    def get_recent_commits(self, start_date, end_date):
        owner, repo = self.repo_url.split("/")[-2:]
        url = f"{self.api_base_url}/repos/{owner}/{repo}/commits"
        params = {"since": start_date.isoformat(), "until": end_date.isoformat()}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_recent_issues(self, start_date, end_date):
        owner, repo = self.repo_url.split("/")[-2:]
        url = f"{self.api_base_url}/repos/{owner}/{repo}/issues"
        params = {"state": "all", "since": start_date.isoformat(), "until": end_date.isoformat()}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_recent_pull_requests(self, start_date, end_date):
        owner, repo = self.repo_url.split("/")[-2:]
        url = f"{self.api_base_url}/repos/{owner}/{repo}/pulls"
        params = {"state": "all", "sort": "updated", "direction": "desc"}
        response = requests.get(url, headers=self.headers, params=params)
        all_prs = response.json()

        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        recent_prs = [pr for pr in all_prs if start_datetime <= datetime.strptime(pr['updated_at'], '%Y-%m-%dT%H:%M:%SZ') <= end_datetime]
        return recent_prs

    def collect_data(self, start_date, end_date):
        data = {
            "repo_info": self.get_repo_info(),
            "recent_commits": self.get_recent_commits(start_date, end_date),
            "recent_issues": self.get_recent_issues(start_date, end_date),
            "recent_pull_requests": self.get_recent_pull_requests(start_date, end_date)
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

    def get_commit_data(self, repo_name, commit_sha):
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(repo_name)
        commit = repo.get_commit(commit_sha)
        
        changes = []
        for file in commit.files:
            changes.append({
                'filename': file.filename,
                'status': file.status,
                'additions': file.additions,
                'deletions': file.deletions,
                'changes': file.changes,
            })
        
        return {
            'message': commit.commit.message,
            'author': commit.commit.author.name,
            'date': commit.commit.author.date,
            'changes': changes,
        }