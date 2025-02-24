import os
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
MODEL_CONFIG = {
    'model': "claude-3-5-sonnet-latest",
    'max_tokens': 8000,
    'temperature': 0
}

APP_CONFIG = {
    'input_directory': '../data/merged_contents',
    'output_directory': '../data/analyzed_contents'
}

# Hardcoded analyzer prompt
SYSTEM_PROMPT = """You are a Funding News Analyzer that only outputs CSV data.

Your task is to analyze funding news articles and extract key information into CSV format.
You must output ONLY the raw CSV data with no additional text, explanations, formatting, or wrapper objects.

Output Format:
- First line: CSV header
- Each subsequent entry on a new line
- Use actual newlines between rows, not \n literals
- No quotes around the entire output

Required columns:
Company,Company Website,Software Category,Founded,Early Adopters/Customers,Raised Amount,Round Type,Funding Date,Lead Investor,Additional Investors

Rules:
1. Only include explicitly stated information
2. Use n/a for missing data
3. Escape commas in fields with double quotes
4. Maintain original capitalization
5. For Additional Investors column, ALWAYS use / to separate multiple investors, never commas (e.g. Ab / Cd / Ef)
6. Keep exact amounts and dates as mentioned
7. Output only the raw CSV data, no wrapper objects or extra formatting
8. Use actual line breaks between rows, not \n escape sequences
9. Format Founded date as Y-M (e.g. 2024-01)

Example output format:
Company,Company Website,Software Category,Founded,Early Adopters/Customers,Raised Amount,Round Type,Funding Date,Lead Investor,Additional Investors
TechCorp,tech.com,AI,2020-03,"Meta, Google",$5M,Seed,2024-03-15,Sequoia,YC / A16Z / Founders Fund"""

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def analyze_content(content):
    """Analyze content using Claude AI and return CSV formatted data"""
    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=MODEL_CONFIG['model'],
            max_tokens=MODEL_CONFIG['max_tokens'],
            temperature=MODEL_CONFIG['temperature'],
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Here is the funding news article to analyze:\n\n{content}"
                }
            ]
        )
        # Handle content which may be a list of TextBlocks
        content_block = message.content[0] if isinstance(message.content, list) else message.content
        # Extract text from TextBlock
        response = content_block.text if hasattr(content_block, 'text') else str(content_block)
        return response.replace('\\n', '\n').strip('"')

    except Exception as e:
        print(f"Error during content analysis: {str(e)}")
        return None

def process_files():
    """Process all merged content files"""
    # Create output directory
    create_directory(APP_CONFIG['output_directory'])
    
    try:
        files = [f for f in os.listdir(APP_CONFIG['input_directory']) if f.endswith('.txt')]
        files.sort()
        
        for file in files:
            print(f"\nProcessing {file}...")
            
            input_path = os.path.join(APP_CONFIG['input_directory'], file)
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = analyze_content(content)
            if analysis:
                output_filename = file.replace('.txt', '_analysis.txt')
                output_path = os.path.join(APP_CONFIG['output_directory'], output_filename)
                
                # Write with newline mode to ensure proper line endings
                with open(output_path, 'w', encoding='utf-8', newline='') as f:
                    f.write(analysis)
                print(f"Analysis saved to {output_filename}")
            else:
                print(f"Failed to analyze {file}")
                
    except Exception as e:
        print(f"Error processing files: {str(e)}")

def main():
    print("Starting content analysis...")
    process_files()
    print("\nContent analysis completed!")

if __name__ == "__main__":
    main() 