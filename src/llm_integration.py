# src/llm_integration.py

import dspy
from config import OPENAI_API_KEY, GPT_MODEL

# Configure DSPy with OpenAI
turbo = dspy.OpenAI(model=GPT_MODEL, api_key=OPENAI_API_KEY)
dspy.settings.configure(lm=turbo)

class CodeAnalyzer(dspy.Signature):
    """Analyze code changes and provide insights."""
    commit_message = dspy.InputField()
    diff = dspy.InputField()
    summary = dspy.OutputField()
    impact = dspy.OutputField()
    code_quality = dspy.OutputField()
    suggestions = dspy.OutputField()

class IssueSummarizer(dspy.Signature):
    """Summarize an issue and provide recommendations."""
    title = dspy.InputField()
    body = dspy.InputField()
    summary = dspy.OutputField()
    priority = dspy.OutputField()
    suggested_action = dspy.OutputField()

class PRAnalyzer(dspy.Signature):
    """Analyze a pull request and provide insights."""
    title = dspy.InputField()
    description = dspy.InputField()
    diff = dspy.InputField()
    summary = dspy.OutputField()
    impact = dspy.OutputField()
    code_quality = dspy.OutputField()
    suggestions = dspy.OutputField()
    related_issues = dspy.OutputField()

def analyze_code_changes(commit_message, diff):
    analyzer = dspy.Predict(CodeAnalyzer)
    result = analyzer(commit_message=commit_message, diff=diff)
    return {
        "summary": result.summary,
        "impact": result.impact,
        "code_quality": result.code_quality,
        "suggestions": result.suggestions
    }

def summarize_issue(title, body):
    summarizer = dspy.Predict(IssueSummarizer)
    result = summarizer(title=title, body=body)
    return {
        "summary": result.summary,
        "priority": result.priority,
        "suggested_action": result.suggested_action
    }

def analyze_pull_request(title, description, diff):
    analyzer = dspy.Predict(PRAnalyzer)
    result = analyzer(title=title, description=description, diff=diff)
    return {
        "summary": result.summary,
        "impact": result.impact,
        "code_quality": result.code_quality,
        "suggestions": result.suggestions,
        "related_issues": result.related_issues
    }
