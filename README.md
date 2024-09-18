# Repository Newsletter Generator

This project generates newsletters based on GitHub repository activity using LLM-powered summaries and insights.

## Setup

1. Create a conda environment:
   ```bash
   conda create -n newsletter_generator python=3.8
   conda activate newsletter_generator
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your GitHub API and OpenAI API credentials in a `.env` file:
   ```
   GITHUB_TOKEN=your_github_token
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Run the application:
   ```bash
   cd src
   python app.py
   ```

## Usage

1. Navigate to the application in your web browser.
2. Enter the repository URL, start date, and end date.
3. Click on "Generate Newsletter" to create your newsletter based on the specified repository activity.

## Features

- Generates newsletters summarizing recent commits, issues, and pull requests.
- Provides insights into repository activity, including top contributors and commit patterns.
- AI-generated summaries for better readability and engagement.

