from flask import Flask, render_template, request, send_file, make_response, session
from company_info_fetcher import CompanyInfoFetcher
from linkedin_formatter import format_linkedin_data
import os
from io import BytesIO
import pdfkit

app = Flask(__name__)
app.secret_key = '1234'  # Ensure you set a secret key for sessions

# Custom filter to check if a variable is a list
@app.template_filter('is_list')
def is_list(value):
    return isinstance(value, list)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_info', methods=['POST'])
def fetch_info():
    company_name = request.form['company_name']
    selected_sources = request.form.getlist('sources')
    analyze_sentiment = 'analyze_sentiment' in request.form
    summarize_news = 'summarize_news' in request.form
    download_format = request.form.get('download_format', 'none')

    fetcher = CompanyInfoFetcher(company_name, selected_sources, analyze_sentiment, summarize_news)
    company_info = fetcher.fetch_all_info()

    if 'Yahoo Finance Data' in company_info and 'Stock Data' in company_info['Yahoo Finance Data']:
        company_info['Yahoo Finance Data']['Stock Data'] = company_info['Yahoo Finance Data']['Stock Data'].to_dict(
            orient='records')

    google_trends_image = company_info.get('Google Trends Image', None)
    google_search_results = company_info.get('Google Search Results', [])
    linkedin_data = format_linkedin_data(company_info.get('LinkedIn Data', {}))
    news_data = company_info.get('News Data', [])
    x_profile = company_info.get('X.com Profile', 'No X.com profile found')
    yahoo_finance_data = company_info.get('Yahoo Finance Data', None)

    # Store the company info and company name in the session for future use in the download route
    session['company_info'] = company_info
    session['company_name'] = company_name

    # Render the results page
    rendered_html = render_template('results.html', company_name=company_name, linkedin_data=linkedin_data,
                                    news_data=news_data, google_trends_image=google_trends_image,
                                    google_search_results=google_search_results, x_profile=x_profile,
                                    yahoo_finance_data=yahoo_finance_data, company_info=company_info)

    # Handle the download after rendering if requested
    if download_format == 'html':
        response = make_response(rendered_html)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = f'attachment; filename={company_name}_info.html'
        return response
    elif download_format == 'pdf':
        pdf = pdfkit.from_string(rendered_html, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={company_name}_info.pdf'
        return response

    # If no download, return the rendered page
    return rendered_html

@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_file(os.path.join(app.root_path, 'static', filename))


if __name__ == '__main__':
    app.run(debug=True)
