# src/main.py

import argparse
from config import REPO_URL, RECIPIENTS, FREQUENCY
from data_collector import GitHubDataCollector
from data_processor import DataProcessor
from llm_integration import generate_newsletter_content
from newsletter_generator import NewsletterGenerator
from email_sender import send_newsletter

def parse_args():
    parser = argparse.ArgumentParser(description="Repository Newsletter Generator")
    parser.add_argument("--repo", required=True, help="GitHub repository URL")
    parser.add_argument("--recipients", help="Comma-separated list of email recipients")
    parser.add_argument("--frequency", choices=['daily', 'weekly'], default='weekly', help="Newsletter frequency")
    parser.add_argument("--view", action="store_true", help="View the newsletter content without sending")
    return parser.parse_args()

def main():
    args = parse_args()
    global REPO_URL, RECIPIENTS, FREQUENCY
    REPO_URL = args.repo
    RECIPIENTS = args.recipients.split(',') if args.recipients else []
    FREQUENCY = args.frequency

    print(f"Generating newsletter for {REPO_URL}")
    if RECIPIENTS:
        print(f"Recipients: {RECIPIENTS}")
    print(f"Frequency: {FREQUENCY}")

    try:
        # Collect data
        collector = GitHubDataCollector(REPO_URL)
        raw_data = collector.collect_data()

        # Process data
        processor = DataProcessor(raw_data)
        processed_data = processor.process_data()

        # Generate content using LLM
        summary, insights = generate_newsletter_content(str(processed_data), str(raw_data))

        # Generate newsletter
        newsletter_gen = NewsletterGenerator(processed_data, summary, insights)
        newsletter_content = newsletter_gen.generate_newsletter()

        if args.view:
            print("\nNewsletter Content:")
            print(newsletter_content)
        elif RECIPIENTS:
            # Send newsletter
            subject = f"Repository Newsletter: {processed_data['repo_name']}"
            send_newsletter(RECIPIENTS, subject, newsletter_content)
            print("Newsletter generated and sent successfully!")
        else:
            print("Newsletter generated but not sent (no recipients specified).")
            print("Use --view to see the content or provide --recipients to send via email.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your GitHub token and repository URL.")

if __name__ == "__main__":
    main()