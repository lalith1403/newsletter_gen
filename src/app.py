from flask import Flask, render_template, request, flash, jsonify
from datetime import datetime, timedelta
import traceback
import logging
import json
from data_collector import GitHubDataCollector
from newsletter_generator import generate_newsletter
from commit_summarizer import summarize_commit, get_commit_diff
from config import GITHUB_TOKEN
from github import Github
from llm_integration import analyze_code_changes, summarize_issue, analyze_pull_request

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Default values
DEFAULT_REPO_URL = "https://github.com/pytorch/pytorch"
DEFAULT_END_DATE = datetime.now().date()
DEFAULT_START_DATE = DEFAULT_END_DATE - timedelta(days=7)

@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.debug("Index route accessed")
    if request.method == 'POST':
        app.logger.debug("POST request received")
        repo_url = request.form['repo_url']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        return generate_result(repo_url, start_date, end_date)
    
    # For GET request, use default values
    return render_template('index.html', 
                           start_date=DEFAULT_START_DATE.strftime('%Y-%m-%d'),
                           end_date=DEFAULT_END_DATE.strftime('%Y-%m-%d'),
                           repo_url=DEFAULT_REPO_URL)

@app.route('/result', methods=['POST'])
def result():
    repo_url = request.form['repo_url']
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
    
    return generate_result(repo_url, start_date, end_date)

def generate_result(repo_url, start_date, end_date):
    try:
        app.logger.debug(f"Generating newsletter for {repo_url} from {start_date} to {end_date}")
        collector = GitHubDataCollector(repo_url)
        data = collector.collect_data(start_date, end_date)
        data['start_date'] = start_date.strftime('%Y-%m-%d')
        data['end_date'] = end_date.strftime('%Y-%m-%d')
        newsletter_content = generate_newsletter(data)
        app.logger.debug("Newsletter generated successfully")
        
        return render_template('result.html', 
                               content=newsletter_content, 
                               commits_json=json.dumps(data['recent_commits'], default=str),
                               issues_json=json.dumps(data['recent_issues'], default=str),
                               pull_requests_json=json.dumps(data.get('recent_pull_requests', []), default=str),
                               repo_info=data['repo_info'])
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        flash(f"An error occurred: {str(e)}")
        return render_template('index.html', 
                               start_date=start_date.strftime('%Y-%m-%d'),
                               end_date=end_date.strftime('%Y-%m-%d'),
                               repo_url=repo_url)

@app.route('/summarize_commit', methods=['POST'])
def summarize_commit_route():
    repo_name = request.form['repo_name']
    commit_sha = request.form['commit_sha']
    
    collector = GitHubDataCollector(f"https://github.com/{repo_name}")
    commit_data = collector.get_commit_data(repo_name, commit_sha)
    commit_data['repo_name'] = repo_name
    commit_data['sha'] = commit_sha
    summary = summarize_commit(commit_data)
    
    return jsonify({'summary': summary})

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    item_type = data['type']
    item_data = data['data']
    
    app.logger.info(f"Processing {item_type}: {item_data.get('sha', item_data.get('number', 'Unknown ID'))}")
    app.logger.debug(f"Raw item data: {json.dumps(item_data, indent=2)}")
    
    summary = ""
    try:
        if item_type == 'commit':
            summary = process_commit(item_data)
        elif item_type == 'issue':
            summary = process_issue(item_data)
        elif item_type == 'pull_request':
            summary = process_pull_request(item_data)
        else:
            raise ValueError(f"Unknown item type: {item_type}")
    except Exception as e:
        app.logger.error(f"Error processing {item_type}: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 400
    
    app.logger.info(f"Processed {item_type} successfully")
    return jsonify({'summary': summary})

def process_commit(commit_data):
    repo_name = commit_data['url'].split('/repos/')[1].split('/commits')[0]
    commit_sha = commit_data['sha']
    
    app.logger.info(f"Fetching diff for commit {commit_sha} in repo {repo_name}")
    diff = get_commit_diff(repo_name, commit_sha)
    
    try:
        analysis = analyze_code_changes(commit_data['commit']['message'], diff)
    except Exception as e:
        app.logger.error(f"Error in AI analysis: {str(e)}")
        analysis = {
            "summary": "AI analysis failed",
            "impact": "Unknown",
            "code_quality": "Unable to assess",
            "suggestions": "No suggestions available due to analysis failure"
        }
    
    summary = f"""
    <div class="space-y-4 overflow-y-auto max-h-full">
        <div class="bg-blue-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">Commit Context</h3>
            <p><strong>Repository:</strong> {repo_name}</p>
            <p><strong>SHA:</strong> {commit_sha[:7]}</p>
            <p><strong>Author:</strong> {commit_data['commit']['author']['name']}</p>
            <p><strong>Date:</strong> {commit_data['commit']['author']['date']}</p>
        </div>
        
        <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">Commit Message</h3>
            <p class="whitespace-pre-wrap">{commit_data['commit']['message']}</p>
        </div>
        
        <div class="bg-green-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">AI Analysis</h3>
            <p><strong>Summary:</strong> {analysis['summary']}</p>
            <p><strong>Impact:</strong> {analysis['impact']}</p>
            <p><strong>Code Quality:</strong> {analysis['code_quality']}</p>
            <p><strong>Suggestions:</strong> {analysis['suggestions']}</p>
        </div>
        
        <div class="bg-yellow-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">Changes</h3>
            <pre class="overflow-x-auto max-h-60 text-sm"><code>{diff}</code></pre>
        </div>
    </div>
    """
    return summary

def process_issue(issue_data):
    try:
        ai_summary = summarize_issue(issue_data['title'], issue_data['body'])
    except Exception as e:
        app.logger.error(f"Error in AI summary: {str(e)}")
        ai_summary = {
            "summary": "AI summary failed",
            "priority": "Unknown",
            "suggested_action": "Unable to suggest action due to summary failure"
        }
    
    summary = f"""
    <div class="space-y-4 overflow-y-auto max-h-full">
        <div class="bg-blue-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">Issue Context</h3>
            <p><strong>Title:</strong> {issue_data['title']}</p>
            <p><strong>Number:</strong> #{issue_data['number']}</p>
            <p><strong>State:</strong> {issue_data['state']}</p>
            <p><strong>Created by:</strong> {issue_data['user']['login']}</p>
            <p><strong>Created at:</strong> {issue_data['created_at']}</p>
        </div>
        
        <div class="bg-green-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">AI Summary</h3>
            <p><strong>Summary:</strong> {ai_summary['summary']}</p>
            <p><strong>Priority:</strong> {ai_summary['priority']}</p>
            <p><strong>Suggested Action:</strong> {ai_summary['suggested_action']}</p>
        </div>
        
        <div class="bg-yellow-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">Description</h3>
            <div class="whitespace-pre-wrap">{issue_data['body']}</div>
        </div>
    </div>
    """
    return summary

def process_pull_request(pr_data):
    repo_name = pr_data['url'].split('/repos/')[1].split('/pulls')[0]
    pr_number = pr_data['number']
    
    app.logger.info(f"Fetching diff for PR #{pr_number} in repo {repo_name}")
    diff = get_pr_diff(repo_name, pr_number)
    
    try:
        analysis = analyze_pull_request(pr_data['title'], pr_data['body'], diff)
    except Exception as e:
        app.logger.error(f"Error in AI analysis: {str(e)}")
        analysis = {
            "summary": "AI analysis failed",
            "impact": "Unknown",
            "code_quality": "Unable to assess",
            "suggestions": "No suggestions available due to analysis failure",
            "related_issues": "Unable to identify related issues"
        }
    
    summary = f"""
    <div class="space-y-4 overflow-y-auto max-h-full">
        <div class="bg-blue-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">Pull Request Context</h3>
            <p><strong>Title:</strong> {pr_data['title']}</p>
            <p><strong>Number:</strong> #{pr_number}</p>
            <p><strong>State:</strong> {pr_data['state']}</p>
            <p><strong>Created by:</strong> {pr_data['user']['login']}</p>
            <p><strong>Created at:</strong> {pr_data['created_at']}</p>
        </div>
        
        <div class="bg-green-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">AI Analysis</h3>
            <p><strong>Summary:</strong> {analysis['summary']}</p>
            <p><strong>Impact:</strong> {analysis['impact']}</p>
            <p><strong>Code Quality:</strong> {analysis['code_quality']}</p>
            <p><strong>Suggestions:</strong> {analysis['suggestions']}</p>
            <p><strong>Related Issues:</strong> {analysis['related_issues']}</p>
        </div>
        
        <div class="bg-yellow-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">Description</h3>
            <div class="whitespace-pre-wrap">{pr_data['body']}</div>
        </div>
        
        <div class="bg-red-50 p-4 rounded-lg">
            <h3 class="text-xl font-bold mb-2">Changes</h3>
            <pre class="overflow-x-auto max-h-60 text-sm"><code>{diff}</code></pre>
        </div>
    </div>
    """
    return summary

def get_pr_diff(repo_name, pr_number):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    return pr.get_files().get_page(0)[0].patch

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error('An error occurred during a request.')
    app.logger.error(traceback.format_exc())
    return "An internal error occurred: " + str(e), 500

@app.template_filter('from_json')
def from_json(value):
    return json.loads(value)

if __name__ == '__main__':
    app.run(debug=True)