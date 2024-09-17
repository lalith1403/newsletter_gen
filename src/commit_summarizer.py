import os
import openai
import dspy
from dotenv import load_dotenv
from github import Github
from config import GITHUB_TOKEN, GPT_MODEL

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up GitHub token
github_token = os.getenv("GITHUB_TOKEN")

class CommitAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.lm = dspy.OpenAI(model="gpt-3.5-turbo")

    def forward(self, commit_message, diff):
        prompt = f"""
        Analyze the following commit:

        Commit message: {commit_message}

        Git diff:
        {diff}

        Provide a structured analysis of this commit, including:
        1. A brief summary of the main changes
        2. The purpose or motivation behind the changes
        3. Any potential impact on the codebase or functionality
        4. Suggestions for code review or testing focus

        Format your response in markdown.
        """

        response = self.lm(prompt)
        return response

def get_commit_diff(repo_name, commit_sha):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    commit = repo.get_commit(commit_sha)
    return commit.files[0].patch if commit.files else "No changes found in this commit."

def summarize_commit(commit_data):
    summary = f"<h3 class='font-semibold'>Commit: {commit_data['sha'][:7]}</h3>"
    summary += f"<p><strong>Author:</strong> {commit_data['commit']['author']['name']}</p>"
    summary += f"<p><strong>Date:</strong> {commit_data['commit']['author']['date']}</p>"
    summary += f"<p><strong>Message:</strong> {commit_data['commit']['message']}</p>"
    
    if 'stats' in commit_data:
        summary += f"<p><strong>Changes:</strong> +{commit_data['stats']['additions']} -{commit_data['stats']['deletions']}</p>"
    
    return summary

def format_changes(changes):
    formatted = []
    for change in changes:
        formatted.append(f"- {change['filename']} ({change['status']}): +{change['additions']}, -{change['deletions']}")
    return "\n".join(formatted)