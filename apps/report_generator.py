import os
from pathlib import Path

# Configuration
CONFIG = {
    'input_directory': '../data/analyzed_contents',
    'output_directory': '../data/reports',
    'output_filename': 'report.txt'
}

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def read_analyzed_files():
    """Read and sort all analyzed files"""
    files = []
    input_dir = Path(CONFIG['input_directory'])
    
    # Get all analysis files and sort them
    for file in input_dir.glob('*_analysis.txt'):
        files.append(file)
    
    return sorted(files)

def merge_analysis_files(files):
    """Merge all analysis files into a single CSV"""
    if not files:
        print("No analysis files found!")
        return None
    
    all_lines = []
    header = None
    
    # Process each file
    for file in files:
        print(f"Processing {file.name}...")
        
        with open(file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
            # Get header from first file
            if header is None and lines:
                header = lines[0]
                all_lines.append(header)
            
            # Add data rows (skip header)
            data_rows = lines[1:] if lines else []
            all_lines.extend(data_rows)
    
    return '\n'.join(all_lines)

def save_report(content):
    """Save the merged content to the report file"""
    if not content:
        return False
    
    try:
        # Create output directory
        create_directory(CONFIG['output_directory'])
        
        # Save merged content
        output_path = os.path.join(CONFIG['output_directory'], CONFIG['output_filename'])
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        
        print(f"\nReport saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error saving report: {str(e)}")
        return False

def main():
    print("Starting report generation...")
    
    # Read all analysis files
    files = read_analyzed_files()
    
    if not files:
        print("No analysis files found!")
        return
    
    # Merge files
    merged_content = merge_analysis_files(files)
    
    # Save report
    if merged_content:
        save_report(merged_content)
        print("\nReport generation completed!")
    else:
        print("\nFailed to generate report!")

if __name__ == "__main__":
    main() 