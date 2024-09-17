# src/data_processor.py

class DataProcessor:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def process_data(self):
        repo_info = self.raw_data.get("repo_info", {})
        commits = self.raw_data.get("recent_commits", [])
        issues = self.raw_data.get("recent_issues", [])

        # Ensure issues is a list
        if isinstance(issues, str):
            print("Warning: Issues data is a string. It might be an error message.")
            issues = []

        return {
            "repo_name": repo_info.get("name", "Unknown"),
            "repo_description": repo_info.get("description", "No description available"),
            "commit_count": len(commits) if isinstance(commits, list) else 0,
            "issue_count": len(issues) if isinstance(issues, list) else 0,
            "open_issue_count": len([i for i in issues if isinstance(i, dict) and i.get("state") == "open"]),
            "closed_issue_count": len([i for i in issues if isinstance(i, dict) and i.get("state") == "closed"]),
            "top_contributors": self.get_top_contributors(commits),
        }

    def get_top_contributors(self, commits, limit=5):
        if not isinstance(commits, list):
            return []
        contributors = {}
        for commit in commits:
            if isinstance(commit, dict) and "commit" in commit:
                author = commit["commit"].get("author", {}).get("name", "Unknown")
                contributors[author] = contributors.get(author, 0) + 1
        return sorted(contributors.items(), key=lambda x: x[1], reverse=True)[:limit]