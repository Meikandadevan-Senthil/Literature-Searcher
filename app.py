from flask import Flask, request, render_template, send_file
import pandas as pd
import requests
from xml.etree import ElementTree
import io
import urllib.parse

app = Flask(__name__)

# Function to search PubMed and retrieve paper IDs
def search_pubmed(keywords, max_results=25):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': keywords,
        'retmax': max_results,
        'retmode': 'xml'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        root = ElementTree.fromstring(response.content)
        ids = [id_elem.text for id_elem in root.findall(".//Id")]
        return ids
    else:
        return []

# Function to fetch article details using PubMed IDs
def fetch_article_details(pmids):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': ','.join(pmids),
        'retmode': 'xml'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.content
    else:
        return None

# Function to extract article titles and links from XML
def extract_article_info(xml_content):
    root = ElementTree.fromstring(xml_content)
    articles = []
    for article in root.findall(".//PubmedArticle"):
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "No Title Available"
        
        pmid_elem = article.find(".//PMID")
        pmid = pmid_elem.text if pmid_elem is not None else "No PMID Available"
        
        articles.append((title, pmid))
    return articles

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords = request.form['keywords']
        num_papers = int(request.form['num_papers'])
        
        pmids = search_pubmed(keywords, max_results=num_papers)
        if pmids:
            xml_content = fetch_article_details(pmids)
            if xml_content:
                articles = extract_article_info(xml_content)
                df = pd.DataFrame(articles, columns=['Title', 'PMID'])
                df['Link'] = 'https://pubmed.ncbi.nlm.nih.gov/' + df['PMID']
                
                # Save DataFrame to CSV in memory
                csv_output = io.BytesIO()
                df.to_csv(csv_output, index=False)
                csv_output.seek(0)
                
                # Pass the CSV data to the template
                return render_template('index.html', csv_data=csv_output.getvalue().decode('utf-8'))
    return render_template('index.html')

@app.route('/download/')
def download():
    csv_data = request.args.get('csv_data')
    if not csv_data:
        return "No CSV data provided", 400

    # Decode URL-encoded CSV data
    csv_data = urllib.parse.unquote(csv_data)
    
    # Convert the CSV string to a BytesIO object
    csv_buffer = io.BytesIO(csv_data.encode('utf-8'))
    return send_file(csv_buffer, 
                     download_name='papers.csv', 
                     as_attachment=True, 
                     mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)
