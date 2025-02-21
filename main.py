import os
from pathlib import Path
from apps import scraper, file_merger, content_analyzer, report_generator

# Get project root directory (where main.py is located)
PROJECT_ROOT = Path(__file__).parent

# Centralized configuration
PIPELINE_CONFIG = {
    'scraper': {
        'base_url': 'https://www.thesaasnews.com/news/seed-round',
        'start_page': 1,
        'end_page': 2,
        'delay_between_pages': 2,  # seconds
        'delay_between_articles': 1,  # seconds
        'data_dir': str(PROJECT_ROOT / 'data' / 'contents'),
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
    },
    'file_merger': {
        'source_directory': str(PROJECT_ROOT / 'data' / 'contents'),
        'output_directory': str(PROJECT_ROOT / 'data' / 'merged_contents')
    },
    'content_analyzer': {
        'model': "claude-3-5-sonnet-latest",
        'max_tokens': 8000,
        'temperature': 0,
        'input_directory': str(PROJECT_ROOT / 'data' / 'merged_contents'),
        'output_directory': str(PROJECT_ROOT / 'data' / 'analyzed_contents')
    },
    'report_generator': {
        'input_directory': str(PROJECT_ROOT / 'data' / 'analyzed_contents'),
        'output_directory': str(PROJECT_ROOT / 'data' / 'reports'),
        'output_filename': 'report.txt'
    }
}

def update_configs():
    """Update configurations for all modules with centralized settings from PIPELINE_CONFIG"""
    scraper.CONFIG.update(PIPELINE_CONFIG['scraper'])
    file_merger.CONFIG.update(PIPELINE_CONFIG['file_merger'])
    # Split content_analyzer config updates for clarity
    content_analyzer.MODEL_CONFIG.update({
        'model': PIPELINE_CONFIG['content_analyzer']['model'],
        'max_tokens': PIPELINE_CONFIG['content_analyzer']['max_tokens'],
        'temperature': PIPELINE_CONFIG['content_analyzer']['temperature']
    })
    content_analyzer.APP_CONFIG.update({
        'input_directory': PIPELINE_CONFIG['content_analyzer']['input_directory'],
        'output_directory': PIPELINE_CONFIG['content_analyzer']['output_directory']
    })
    report_generator.CONFIG.update(PIPELINE_CONFIG['report_generator'])

def create_directories():
    """Create all necessary directories"""
    directories = [
        'data/contents',
        'data/merged_contents',
        'data/analyzed_contents',
        'data/reports'
    ]
    for path in directories:
        os.makedirs(PROJECT_ROOT / path, exist_ok=True)

def main():
    # Update configurations
    update_configs()
    
    # Create necessary directories
    create_directories()

    print("\n=== Starting SaaS News Pipeline ===\n")

    print("Step 1: Web Scraping")
    print("=====================")
    scraper.main()

    print("\nStep 2: File Merging")
    print("===================")
    file_merger.main()

    print("\nStep 3: Content Analysis")
    print("======================")
    content_analyzer.main()

    print("\nStep 4: Report Generation")
    print("=======================")
    report_generator.main()

    print("\n=== Pipeline Completed Successfully ===")

if __name__ == "__main__":
    main() 