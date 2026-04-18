#!/usr/bin/env python3
"""
PlantUML Converter - uses UUID to avoid server cache
"""

import sys
import base64
import zlib
import requests
import uuid

def encode_puml(content):
    """DEFLATE encoding with leading dash"""
    compressed = zlib.compress(('-' + content).encode('utf-8'), 9)
    encoded = base64.b64encode(compressed).decode('utf-8').replace('+', '-').replace('/', '_').replace('=', '')
    return '~1' + encoded

def convert_puml(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        puml_code = f.read()
    
    # Add UUID to guarantee unique request (avoids PlantUML server cache)
    unique_content = puml_code.strip() + f"\n' uuid: {uuid.uuid4()}"
    
    encoded = encode_puml(unique_content)
    print(f"Encoded length: {len(encoded)}")
    
    url = f"https://www.plantuml.com/plantuml/svg/{encoded}"
    
    response = requests.get(url, headers={'Accept-Encoding': 'identity'}, timeout=60)
    
    if response.status_code == 200:
        if '<svg' in response.text[:100]:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Success! {output_file} ({len(response.content)} bytes)")
            return True
        else:
            print(f"Error: Not SVG - {response.text[:200]}")
            return False
    else:
        print(f"HTTP Error: {response.status_code}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python plantuml_converter.py input.puml output.svg")
        sys.exit(1)
    
    success = convert_puml(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)