import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time

# Configuration
CONFIG = {
    'base_url': 'https://www.thesaasnews.com/news/seed-round',
    'start_page': 1,
    'end_page': 2,
    'delay_between_pages': 2,  # seconds
    'delay_between_articles': 1,  # seconds
    'data_dir': '../data/contents',
    'excluded_urls': [
        'thesaasnews.com/news/growth-round',
        'thesaasnews.com/news/private-equity-investment',
        'thesaasnews.com/news/series-a',
        'thesaasnews.com/news/series-b',
        'thesaasnews.com/news/series-c',
        'thesaasnews.com/news/series-d',
        'thesaasnews.com/news/series-e',
        'thesaasnews.com/news/series-f'
    ]
}

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def clean_filename(title):
    """Convert title to a valid filename"""
    # Remove special characters and replace spaces with underscores
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'[-\s]+', '_', filename).strip('-').lower()
    return filename + '.txt'

def scrape_article(url):
    """Scrape individual article content"""
    try:
        # Add delay between article requests
        time.sleep(CONFIG['delay_between_articles'])
        
        # Get the preview page first
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get article title
        title = soup.find('h1').text.strip()
        
        # Find the "Continue reading" link
        continue_link = soup.find('a', string='Continue reading')
        if continue_link:
            # Get the full article URL
            full_article_url = urljoin(url, continue_link['href'])
            
            # Get the full article page
            response = requests.get(full_article_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get article content
        article_content = []
        
        # Add title
        article_content.append(title + '\n\n')
        
        # Get author and date if available
        meta_info = soup.find('div', string=lambda text: 'by' in str(text).lower())
        if meta_info:
            article_content.append(meta_info.text.strip() + '\n\n')
        
        # Get main content - look for the article content container
        article_container = soup.find('article') or soup.find('div', class_='post-content')
        if article_container:
            # Get all text content within the article
            main_content = article_container.find_all(['p', 'h2', 'h3', 'ul', 'ol'])
            for content in main_content:
                if content.text.strip():
                    # Handle lists specially
                    if content.name in ['ul', 'ol']:
                        list_items = content.find_all('li')
                        for item in list_items:
                            article_content.append(f"• {item.text.strip()}\n")
                        article_content.append('\n')
                    else:
                        article_content.append(content.text.strip() + '\n\n')
        
        return title, ''.join(article_content)
    except Exception as e:
        print(f"Error scraping article {url}: {str(e)}")
        return None, None

def should_skip_url(url):
    """Check if URL should be skipped"""
    return any(excluded in url.lower() for excluded in CONFIG['excluded_urls'])

def scrape_page(base_url, page_num=None):
    """Scrape articles from a specific page"""
    try:
        # Construct page URL
        page_url = base_url
        if page_num and page_num > 1:
            page_url = f"{base_url}?page={page_num}"
        
        print(f"Scraping page {page_num if page_num else 1}...")
        
        # Add delay between page requests
        time.sleep(CONFIG['delay_between_pages'])
        
        # Get the page
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article links
        articles = soup.find_all('a', href=lambda href: href and 'news' in href)
        article_links = set()
        
        # Extract unique article URLs, excluding the specified ones
        for article in articles:
            article_url = urljoin(base_url, article['href'])
            if 'page=' not in article_url and not should_skip_url(article_url):
                article_links.add(article_url)
        
        return article_links
    
    except Exception as e:
        print(f"Error scraping page {page_num}: {str(e)}")
        return set()

def process_page(page_num):
    """Process a single page and save its articles"""
    # Create directory for this page
    page_dir = os.path.join(CONFIG['data_dir'], f'page_{page_num}')
    create_directory(page_dir)
    
    # Get article links from current page
    page_links = scrape_page(CONFIG['base_url'], page_num)
    
    if not page_links:
        print(f"No articles found on page {page_num}")
        return False
    
    print(f"\nFound {len(page_links)} articles on page {page_num}")
    
    # Scrape each article
    for i, article_url in enumerate(page_links, 1):
        print(f"\nProcessing article {i} of {len(page_links)} on page {page_num}")
        title, content = scrape_article(article_url)
        if title and content:
            filename = clean_filename(title)
            filepath = os.path.join(page_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved article: {filename}")
    
    return True

def main():
    # Create main data directory
    create_directory(CONFIG['data_dir'])
    
    # Process each page
    for page_num in range(CONFIG['start_page'], CONFIG['end_page'] + 1):
        print(f"\n{'='*50}")
        print(f"Processing page {page_num}")
        print(f"{'='*50}\n")
        
        success = process_page(page_num)
        
        # If no articles found, might have reached the end
        if not success:
            print(f"No articles found on page {page_num}, stopping.")
            break

if __name__ == "__main__":
    main() 