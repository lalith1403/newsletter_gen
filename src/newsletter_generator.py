# src/newsletter_generator.py

from datetime import datetime
from collections import Counter
import re

def generate_newsletter(data):
    repo_info = data['repo_info']
    recent_commits = data['recent_commits']
    recent_issues = data['recent_issues']
    recent_pull_requests = data['recent_pull_requests']

    # Calculate top contributors
    contributors = Counter(commit['commit']['author']['name'] for commit in recent_commits)
    top_contributors = contributors.most_common(5)

    # Analyze commits for patterns and significant changes
    commit_patterns = analyze_commits(recent_commits)
    
    # Analyze issues for common themes and critical problems
    issue_themes = analyze_issues(recent_issues)

    newsletter = f"""
    <h1 class="text-3xl font-bold mb-4">{repo_info['full_name']} Newsletter</h1>
    <p class="mb-4"><strong>Description:</strong> {repo_info['description']}</p>
    
    <h2 class="text-2xl font-semibold mt-6 mb-2">Summary</h2>
    <p>From {data['start_date']} to {data['end_date']}:</p>
    <ul class="list-disc pl-5 mb-4">
        <li>{len(recent_commits)} new commits</li>
        <li>{len(recent_issues)} issues updated</li>
        <li>{len(recent_pull_requests)} pull requests updated</li>
    </ul>
    
    <h2 class="text-2xl font-semibold mt-6 mb-2">Insights</h2>
    <ul class="list-disc pl-5 mb-4">
        <li>The repository has {repo_info['stargazers_count']} stars and {repo_info['forks_count']} forks.</li>
        <li>There are currently {repo_info['open_issues_count']} open issues.</li>
        <li>The repository is written primarily in {repo_info['language']}.</li>
    </ul>
    
    <h2 class="text-2xl font-semibold mt-6 mb-2">Recent Activity</h2>
    <h3 class="text-xl font-semibold mt-4 mb-2">Commit Patterns and Significant Changes</h3>
    <ul class="list-disc pl-5 mb-4">
    """

    for pattern, commits in commit_patterns.items():
        newsletter += f"<li><strong>{pattern}:</strong> {commits}</li>\n"

    newsletter += """
    </ul>
    
    <h3 class="text-xl font-semibold mt-4 mb-2">Issue Themes and Critical Problems</h3>
    <ul class="list-disc pl-5 mb-4">
    """

    for theme, issues in issue_themes.items():
        newsletter += f"<li><strong>{theme}:</strong> {issues}</li>\n"

    newsletter += """
    </ul>
    
    <h2 class="text-2xl font-semibold mt-6 mb-2">Top Contributors</h2>
    <ul class="list-disc pl-5 mb-4">
    """

    for contributor, count in top_contributors:
        newsletter += f"<li>{contributor}: {count} commits</li>\n"

    newsletter += f"""
    </ul>
    
    <p class="mt-6"><em>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    """

    return newsletter

def analyze_commits(commits):
    patterns = {
        "Bug Fixes": [],
        "Feature Additions": [],
        "Performance Improvements": [],
        "Documentation Updates": [],
        "Refactoring": [],
        "Other": []
    }
    
    for commit in commits:
        message = commit['commit']['message'].lower()
        if re.search(r'fix|bug|issue', message):
            patterns["Bug Fixes"].append(commit['commit']['message'])
        elif re.search(r'feat|add|new', message):
            patterns["Feature Additions"].append(commit['commit']['message'])
        elif re.search(r'perf|optimiz|improv', message):
            patterns["Performance Improvements"].append(commit['commit']['message'])
        elif re.search(r'doc|readme', message):
            patterns["Documentation Updates"].append(commit['commit']['message'])
        elif re.search(r'refactor|clean|reorganiz', message):
            patterns["Refactoring"].append(commit['commit']['message'])
        else:
            patterns["Other"].append(commit['commit']['message'])
    
    return {k: summarize_commits(v) for k, v in patterns.items() if v}

def summarize_commits(commits):
    if len(commits) == 1:
        return commits[0]
    elif len(commits) <= 3:
        return ", ".join(commits)
    else:
        return f"{len(commits)} commits, including: {', '.join(commits[:2])}..."

def analyze_issues(issues):
    themes = {
        "Critical Bugs": [],
        "Feature Requests": [],
        "Performance Issues": [],
        "Documentation Needs": [],
        "Other": []
    }
    
    for issue in issues:
        title = issue['title'].lower()
        if re.search(r'critical|urgent|important|severe', title):
            themes["Critical Bugs"].append(issue['title'])
        elif re.search(r'feature|request|enhancement', title):
            themes["Feature Requests"].append(issue['title'])
        elif re.search(r'performance|slow|optimization', title):
            themes["Performance Issues"].append(issue['title'])
        elif re.search(r'doc|readme|tutorial', title):
            themes["Documentation Needs"].append(issue['title'])
        else:
            themes["Other"].append(issue['title'])
    
    return {k: summarize_issues(v) for k, v in themes.items() if v}

def summarize_issues(issues):
    if len(issues) == 1:
        return issues[0]
    elif len(issues) <= 3:
        return ", ".join(issues)
    else:
        return f"{len(issues)} issues, including: {', '.join(issues[:2])}..."