#!/usr/bin/env python3
"""
Mermaid Converter - wrapper around mmdc for generating diagrams
Usage: python mermaid_converter.py input.mmd output.svg [width]
"""

import sys
import os
import subprocess

def convert_mermaid(input_file, output_file, width=1200):
    """Convert .mmd file to SVG using mmdc"""
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        return False
    
    # Check if mmdc is available
    try:
        subprocess.run(['mmdc', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: mmdc not found. Install with:")
        print("  npm install -g @mermaid-js/mermaid-cli")
        return False
    
    # Run mmdc
    cmd = ['mmdc', '-i', input_file, '-o', output_file, '-w', str(width), '-b', 'white']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Success! Generated: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python mermaid_converter.py input.mmd output.svg [width]")
        print("Example: python mermaid_converter.py diagram.mmd diagram.svg 1200")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    
    success = convert_mermaid(input_file, output_file, width)
    sys.exit(0 if success else 1)