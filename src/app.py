from flask import Flask, render_template, request, flash
from main import generate_newsletter
from datetime import datetime, timedelta
import traceback
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.debug("Index route accessed")
    if request.method == 'POST':
        app.logger.debug("POST request received")
        repo_url = request.form['repo_url']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        try:
            app.logger.debug(f"Generating newsletter for {repo_url} from {start_date} to {end_date}")
            newsletter_content = generate_newsletter(repo_url, start_date, end_date)
            app.logger.debug("Newsletter generated successfully")
            return render_template('result.html', content=newsletter_content)
        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            app.logger.error(traceback.format_exc())
            flash(f"An error occurred: {str(e)}")
            return render_template('index.html')
    
    # For GET request, set default date range to last 7 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    app.logger.debug(f"Rendering index template with start_date={start_date} and end_date={end_date}")
    return render_template('index.html', start_date=start_date, end_date=end_date)

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error('An error occurred during a request.')
    app.logger.error(traceback.format_exc())
    return "An internal error occurred: " + str(e), 500

if __name__ == '__main__':
    app.run(debug=True)