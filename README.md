# SaaS Pulse

A data pipeline to mine and analyze SaaS startup funding news and partnerships. The system scrapes startup funding announcements, extracts relevant content, and uses AI to analyze funding details and business relationships.

## Setup

Create a `.env` file in the project root directory with:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Pipeline Components

1. **Web Scraping** (scraper.py)
   - Scrapes SaaS News for seed round funding announcements
   - Filters out non-seed round content
   - Stores raw article content in `data/contents/`

2. **Content Merging** (file_merger.py)
   - Combines scraped articles from each page
   - Groups content by page for efficient processing
   - Outputs to `data/merged_contents/`

3. **Content Analysis** (content_analyzer.py)
   - Uses Claude 3.5 Sonnet to analyze funding details
   - Extracts structured data from articles
   - Stores analysis in `data/analyzed_contents/`

4. **Report Generation** (report_generator.py)
   - Merges analyzed data into comprehensive reports
   - Creates consolidated CSV output
   - Saves reports to `data/reports/`

## Output Format

The pipeline generates CSV reports containing:
- Company name and website
- Software category
- Founding date
- Early adopters/customers
- Funding details (amount, round type, date)
- Lead investor
- Additional investors

Reports are stored in `data/reports/` for easy analysis.

## Configuration

The pipeline is configurable through `main.py`, including:
- Scraping parameters (URLs, delays, exclusions)
- File paths and directory structure
- AI model settings (Claude 3.5 Sonnet)
- Output formats and locations