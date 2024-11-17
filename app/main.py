#pip install Scrapy
#pip install beautifulsoup4
import scrapy
from bs4 import BeautifulSoup


import requests

def print_tags_with_class(tag, depth=0):
    indent = '--' * depth  # Indentation for hierarchy
    class_name = tag.get('class', [])  # Get class as a list
    class_str = f" (class: {' '.join(class_name)})" if class_name else ""  # Format class
    print(f"{indent}{tag.name}{class_str}")  # Print tag name with class

    # Iterate through children of the current tag
    for child in tag.children:
        if child.name:  # Only process tags (skip text or comments)
            print_tags_with_class(child, depth + 1)



def extraction_job():
    url = "https://dribbble.com/jobs?keyword=&location="
    res = requests.get(url)
    print(res.status_code)
    raw_html = BeautifulSoup(res.text , 'html.parser')
    # Start from the root element
    print_tags_with_class(raw_html.body)
    target_div = raw_html.find('div', class_="flushed")
    print(target_div)
    if target_div:
        h4_tags = target_div.find_all('h4')  # Find all <h4> tags within the div
        for h4 in h4_tags:
            print(h4.text.strip())  # Print the text content of each <h4>
    else:
        print("Target div not found")


extraction_job()