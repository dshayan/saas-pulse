# SaaS Pulse

A data pipeline to mine and analyze SaaS startup funding news and partnerships. The system scrapes startup funding announcements, extracts relevant content, and uses AI to analyze funding details and business relationships.

## Pipeline Components & Flow

1. **Web Scraping** (scraper.py): Scrapes SaaS News for seed round funding announcements
2. **Content Merging** (file_merger.py): Combines scraped articles from each page for efficient processing
3. **Content Analysis** (content_analyzer.py): Uses AI to analyze contents and extracts structured data
4. **Report Generation** (report_generator.py): Merges analyzed data into comprehensive reports

## Configuration

The pipeline is configurable through a central configuration in main.py, including:
- Scraping parameters (URLs, delays, exclusions)
- File paths and directory structure
- AI model settings (Claude 3.5 Sonnet)
- Output formats and locations

### Environment Variables

Create a `.env` file in the project root directory with:
```
ANTHROPIC_API_KEY=your_api_key_here
```