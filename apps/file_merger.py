import os

# Configuration
CONFIG = {
    'source_directory': '../data/contents',
    'output_directory': '../data/merged_contents'
}

def merge_text_files(source_dir, output_dir):
    """
    Merge text files from each page directory into separate merged files.
    Each page directory's contents are combined into a single file with separators.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process each page directory
    for page_dir in sorted(d for d in os.listdir(source_dir) if d.startswith('page_')):
        page_path = os.path.join(source_dir, page_dir)
        if not os.path.isdir(page_path):
            continue
        
        txt_files = sorted(f for f in os.listdir(page_path) if f.endswith('.txt'))
        if not txt_files:
            print(f"No text files found in {page_dir}")
            continue
        
        output_file = os.path.join(output_dir, f"{page_dir}.txt")
        print(f"Merging files from {page_dir}...")
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, filename in enumerate(txt_files):
                with open(os.path.join(page_path, filename), 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                if i < len(txt_files) - 1:
                    outfile.write('\n\n----------\n\n')
        
        print(f"Created {output_file}")

def main():
    print("Starting file merger...")
    merge_text_files(CONFIG['source_directory'], CONFIG['output_directory'])
    print("\nAll files have been merged successfully!")

if __name__ == "__main__":
    main() 