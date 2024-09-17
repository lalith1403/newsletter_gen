# src/newsletter_generator.py

class NewsletterGenerator:
    def __init__(self, processed_data, summary, insights):
        self.processed_data = processed_data
        self.summary = summary
        self.insights = insights

    def generate_newsletter(self):
        newsletter_content = f"""
        <html>
        <body>
        <h1>Repository Newsletter: {self.processed_data['repo_name']}</h1>
        
        <h2>Summary</h2>
        <p>{self.summary}</p>
        
        <h2>Insights</h2>
        <p>{self.insights}</p>
        
        <h2>Recent Activity</h2>
        <ul>
            <li>Commits: {self.processed_data['commit_count']}</li>
            <li>Total Issues: {self.processed_data['issue_count']}</li>
            <li>Open Issues: {self.processed_data['open_issue_count']}</li>
            <li>Closed Issues: {self.processed_data['closed_issue_count']}</li>
        </ul>
        
        <h2>Top Contributors</h2>
        <ul>
        {"".join(f"<li>{name}: {count} commits</li>" for name, count in self.processed_data['top_contributors'])}
        </ul>
        
        <p>Repository Description: {self.processed_data['repo_description']}</p>
        </body>
        </html>
        """
        return newsletter_content