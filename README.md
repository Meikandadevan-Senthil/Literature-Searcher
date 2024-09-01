# PubMed Article Search Flask Application

This is a simple Flask web application that allows users to search for PubMed articles based on keywords and download the results as a CSV file. The application uses PubMed's E-utilities API to fetch article information and provides a user-friendly interface to display and download the search results.

## Features

- Search for PubMed articles using keywords.
- Fetch article details including titles and PMIDs.
- Display search results in a tabular format on the web page.
- Download search results as a CSV file.

## Requirements

- Python 3.6 or higher
- Flask
- Pandas
- Requests

You can install the required packages using pip:

```bash
pip install Flask pandas requests
```

## How to Run the Application

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Meikandadevan-Senthil/Literature-Searcher
   cd Literature-Searcher
   ```

2. **Run the Flask Application**

   ```bash
   python app.py
   ```

   The application will start and be accessible at `http://127.0.0.1:5000/`.

## Usage

1. **Search for Articles**

   - Open the application in your web browser.
   - Enter the keywords for the PubMed search in the input field.
   - Specify the number of results to retrieve.
   - Click the "Search" button to view the results.

2. **Download Results**

   - After performing the search, the results will be displayed on the page.
   - Click the "Download" link to get a CSV file containing the article titles and PMIDs.

## Endpoints

- `/` (GET, POST): The main page where users can enter search keywords and specify the number of results. The results are displayed in a table format, and a CSV download link is provided.
- `/download/` (GET): Endpoint to download the CSV file containing the search results.

## Code Overview

- **search_pubmed(keywords, max_results=25)**: Searches PubMed for articles matching the provided keywords and returns a list of article IDs.
- **fetch_article_details(pmids)**: Fetches detailed information for the provided PubMed IDs.
- **extract_article_info(xml_content)**: Extracts article titles and PMIDs from the XML response returned by PubMed.
- **index()**: Handles the main page logic, including form submission and result display.
- **download()**: Handles CSV file downloads.

## Contact

For any questions or issues, please contact meikandadevan.senthil@gmail.com
