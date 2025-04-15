from flask import Flask, render_template, request, send_file, make_response, session
from company_info_fetcher import CompanyInfoFetcher
from linkedin_formatter import format_linkedin_data
import os

app = Flask(__name__)
app.secret_key = '1234'

@app.template_filter('is_list')
def is_list(value):
    return isinstance(value, list)

app = Flask(__name__)
app.secret_key = '1234'

@app.route('/')
def index():
    report_downloaded = session.pop('report_downloaded', False)
    return render_template('index.html', report_downloaded=report_downloaded)

@app.route('/fetch_info', methods=['POST'])
def fetch_info():
    company_name = request.form['company_name']
    selected_sources = request.form.getlist('sources')
    analyze_sentiment = 'analyze_sentiment' in request.form
    summarize_news = 'summarize_news' in request.form
    download_report = 'download_report' in request.form

    fetcher = CompanyInfoFetcher(company_name, selected_sources, analyze_sentiment, summarize_news)
    company_info = fetcher.fetch_all_info()

    linkedin_data = format_linkedin_data(company_info.get('LinkedIn Data', {}))
    news_data = company_info.get('News Data', [])
    google_search_results = company_info.get('Google Search Results', [])
    google_trends_image = company_info.get('Google Trends Image', None)
    trustpilot_data = company_info.get('Trustpilot Data', [])
    if isinstance(trustpilot_data, str):
        trustpilot_data = []

    rendered_html = render_template(
        'results.html',
        company_name=company_name,
        linkedin_data=linkedin_data,
        news_data=news_data,
        google_search_results=google_search_results,
        google_trends_image=google_trends_image,
        company_info=company_info,
        trustpilot_data=trustpilot_data,
    )

    if download_report:
        session['report_downloaded'] = True
        response = make_response(rendered_html)
        response.headers['Content-Disposition'] = f'attachment; filename="{company_name}_report.html"'
        response.headers['Content-Type'] = 'text/html'
        return response

    return rendered_html



@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_file(os.path.join(app.root_path, 'static', filename))

if __name__ == '__main__':
    app.run(debug=True)
