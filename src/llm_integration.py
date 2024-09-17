# src/llm_integration.py

import dspy
from config import OPENAI_API_KEY

dspy.settings.configure(lm="openai", api_key=OPENAI_API_KEY)

class RepoSummarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarizer = dspy.ChainOfThought("summarize")

    def forward(self, repo_data):
        summary = self.summarizer(f"Summarize the following repository data:\n{repo_data}")

        dspy.Suggest(
            "The summary should be concise and highlight key points.",
            "Consider mentioning major changes, trends, and notable contributions."
        )

        dspy.Assert(
            len(summary.split()) <= 100,
            "The summary should be no longer than 100 words."
        )

        return summary

class InsightGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.insight_gen = dspy.ChainOfThought("generate_insights")

    def forward(self, repo_summary, metrics):
        insights = self.insight_gen(f"Generate insights based on this summary and metrics:\nSummary: {repo_summary}\nMetrics: {metrics}")

        dspy.Suggest(
            "Insights should be actionable and relevant to the development team.",
            "Try to identify patterns or areas for improvement."
        )

        dspy.Assert(
            len(insights.split('\n')) >= 3,
            "Generate at least 3 distinct insights."
        )

        return insights

def generate_newsletter_content(repo_data, metrics):
    summarizer = RepoSummarizer()
    insight_generator = InsightGenerator()

    summary = summarizer(repo_data)
    insights = insight_generator(summary, metrics)

    return summary, insights
