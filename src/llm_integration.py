# src/llm_integration.py

import dspy
from config import OPENAI_API_KEY

# Configure DSPy with OpenAI
turbo = dspy.OpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
dspy.settings.configure(lm=turbo)

class RepoInsights(dspy.Signature):
    """Generate insights and analysis for a GitHub repository based on recent activity."""
    repo_data = dspy.InputField(desc="Processed data about the repository")
    summary = dspy.OutputField(desc="A concise summary of the repository's recent activity")
    key_insights = dspy.OutputField(desc="List of key insights about the repository's activity")
    trend_analysis = dspy.OutputField(desc="Analysis of trends in commit activity and issue management")
    recommendations = dspy.OutputField(desc="Actionable recommendations for repository maintainers")

class InsightGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.Predict(RepoInsights)

    def forward(self, repo_data):
        return self.generate(repo_data=repo_data)

def generate_newsletter_content(processed_data, raw_data):
    insight_generator = InsightGenerator()
    result = insight_generator(repo_data=processed_data)
    
    key_insights_html = "".join(f'<li>{insight}</li>' for insight in result.key_insights.split('\n') if insight)
    recommendations_html = "".join(f'<li>{recommendation}</li>' for recommendation in result.recommendations.split('\n') if recommendation)
    
    newsletter_content = f"""
    <h2 class="text-2xl font-semibold mt-6 mb-2">Summary</h2>
    <p>{result.summary}</p>
    
    <h2 class="text-2xl font-semibold mt-6 mb-2">Key Insights</h2>
    <ul class="list-disc pl-5 space-y-2">
        {key_insights_html}
    </ul>
    
    <h2 class="text-2xl font-semibold mt-6 mb-2">Trend Analysis</h2>
    <p>{result.trend_analysis}</p>
    
    <h2 class="text-2xl font-semibold mt-6 mb-2">Recommendations</h2>
    <ul class="list-disc pl-5 space-y-2">
        {recommendations_html}
    </ul>
    """
    
    return newsletter_content
