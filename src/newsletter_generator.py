# src/newsletter_generator.py

class NewsletterGenerator:
    def __init__(self, processed_data, newsletter_content):
        self.processed_data = processed_data
        self.newsletter_content = newsletter_content

    def generate_newsletter(self):
        newsletter_content = f"""
        <h1 class="text-3xl font-bold mb-4">Repository Newsletter: {self.processed_data['repo_name']}</h1>
        
        {self.newsletter_content}
        
        <h2 class="text-2xl font-semibold mt-6 mb-2">Recent Activity</h2>
        <ul class="list-disc pl-5 space-y-2">
            <li>Commits: {self.processed_data['commit_count']}</li>
            <li>Total Issues: {self.processed_data['issue_count']}</li>
            <li>Open Issues: {self.processed_data['open_issue_count']}</li>
            <li>Closed Issues: {self.processed_data['closed_issue_count']}</li>
        </ul>
        
        <h2 class="text-2xl font-semibold mt-6 mb-2">Top Contributors</h2>
        <ul class="list-disc pl-5 space-y-2">
        {"".join(f"<li>{name}: {count} commits</li>" for name, count in self.processed_data['top_contributors'])}
        </ul>
        
        <p class="mt-6"><strong>Repository Description:</strong> {self.processed_data['repo_description']}</p>
        """
        return newsletter_content