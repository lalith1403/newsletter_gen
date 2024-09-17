# src/main.py

import argparse
from config import REPO_URL, RECIPIENTS, FREQUENCY
from data_collector import GitHubDataCollector

def parse_args():
    parser = argparse.ArgumentParser(description="Repository Newsletter Generator")
    parser.add_argument("--repo", required=True, help="GitHub repository URL")
    parser.add_argument("--recipients", required=True, help="Comma-separated list of email recipients")
    parser.add_argument("--frequency", choices=['daily', 'weekly'], default='weekly', help="Newsletter frequency")
    return parser.parse_args()

def main():
    args = parse_args()
    global REPO_URL, RECIPIENTS, FREQUENCY
    REPO_URL = args.repo
    RECIPIENTS = args.recipients.split(',')
    FREQUENCY = args.frequency

    print(f"Generating newsletter for {REPO_URL}")
    print(f"Recipients: {RECIPIENTS}")
    print(f"Frequency: {FREQUENCY}")

    collector = GitHubDataCollector(REPO_URL)
    data = collector.collect_data()

    print("Collected data:")
    print(f"Repo info: {data['repo_info']['name']}")
    print(f"Recent commits: {len(data['recent_commits'])}")
    print(f"Recent issues: {len(data['recent_issues'])}")

if __name__ == "__main__":
    main()
