# src/llm_integration.py

import dspy
from config import OPENAI_API_KEY

# Configure DSPy with OpenAI
turbo = dspy.OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
dspy.settings.configure(lm=turbo)

class GenerateContent(dspy.Signature):
    """Generate a summary and insights for a GitHub repository newsletter."""
    context = dspy.InputField(desc="Processed data about the repository")
    summary = dspy.OutputField(desc="A concise summary of the repository's recent activity")
    insights = dspy.OutputField(desc="Insights and analysis based on the repository data")

class NewsletterContent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.Predict(GenerateContent)

    def forward(self, context):
        return self.generate(context=context)

def generate_newsletter_content(processed_data, raw_data):
    newsletter_content = NewsletterContent()
    result = newsletter_content(context=processed_data)
    return result.summary, result.insights
