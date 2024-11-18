# Import necessary libraries
# Install required libraries using:
# pip install requests
# pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup

# Global Configurations
TARGET_URL = "https://dribbble.com/jobs?keyword=&location="
USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def fetch_webpage(url):

    try:
        response = requests.get(url, headers=USER_AGENT)
        response.raise_for_status()  # Raise HTTP errors if any
        print(f"[INFO] Successfully fetched the webpage: {url}")
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch the URL: {e}")
        return None

def extract_tags_with_class(tag, depth=0):
    indent = '--' * depth  # Indentation for hierarchy
    class_name = tag.get('class', [])  # Get class as a list
    class_str = f" (class: {' '.join(class_name)})" if class_name else ""  # Format class
    print(f"{indent}{tag.name}{class_str}")

    # Process child tags
    for child in tag.children:
        if child.name:  # Skip text or comments
            extract_tags_with_class(child, depth + 1)

def extract_target_content(raw_html, target_div_class):

    print("[INFO] Searching for the target content...")
    target_div = raw_html.find('div', class_=target_div_class)
    if target_div:
        job_titles = [h4.text.strip() for h4 in target_div.find_all('h4')]
        return job_titles
    else:
        print("[WARNING] Target div not found.")
        return []

def save_results_to_file(results, file_name="job_titles.txt"):

 
    try:
        with open(file_name, 'w') as file:
            file.write("\n".join(results))
        print(f"[INFO] Results saved to {file_name}")
    except Exception as e:
        print(f"[ERROR] Failed to save results to file: {e}")

def run_scraper():

    print("[INFO] Starting the web scraping process...")

    raw_html = fetch_webpage(TARGET_URL)
    if raw_html is None:
        print("[ERROR] Web scraping aborted due to failed fetch.")
        return


    print("[INFO] Printing HTML structure (truncated):")
    extract_tags_with_class(raw_html.body, depth=0)

    job_titles = extract_target_content(raw_html, target_div_class="flushed")
    if job_titles:
        print(f"[INFO] Extracted {len(job_titles)} job titles:")
        for title in job_titles:
            print(f" - {title}")

        save_results_to_file(job_titles)
    else:
        print("[INFO] No job titles extracted.")

if __name__ == "__main__":
    run_scraper()
