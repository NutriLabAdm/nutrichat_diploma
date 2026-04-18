#!/usr/bin/env python3
"""
Конвертер SVG в PNG с использованием Pillow.
SVG парсится вручную и рендерится через Pillow.

Использование:
    python svg2png_converter.py input.svg [output.png]
    python svg2png_converter.py input.svg output.png [--scale=2]

Примеры:
    python svg2png_converter.py diagram.svg
    python svg2png_converter.py diagram.svg diagram.png
    python svg2png_converter.py diagram.svg --scale=2
"""

import os
import sys
import re
import argparse
from PIL import Image, ImageDraw, ImageFont


def parse_color(color_str):
    """Преобразование цвета из SVG в RGB."""
    color_str = color_str.strip().lower()
    
    if color_str.startswith('#'):
        hex_color = color_str[1:]
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3:
            return tuple(int(c*2, 16) for c in hex_color)
    elif color_str.startswith('rgb'):
        match = re.search(r'(\d+),\s*(\d+),\s*(\d+)', color_str)
        if match:
            return tuple(int(m) for m in match.groups())
    
    # Named colors
    named = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'gray': (128, 128, 128),
    }
    return named.get(color_str, (0, 0, 0))


def svg_to_png(svg_path, png_path=None, scale=1):
    """Конвертация SVG в PNG."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    
    # Parse viewBox
    viewbox_match = re.search(r'viewBox=["\'](\d+)\s+(\d+)\s+(\d+)\s+(\d+)["\']', svg_content)
    if viewbox_match:
        _, _, width, height = map(int, viewbox_match.groups())
    else:
        width, height = 800, 400
    
    width *= scale
    height *= scale
    
    # Parse width/height from svg tag
    w_match = re.search(r'<svg[^>]*\swidth=["\'](\d+)', svg_content)
    h_match = re.search(r'<svg[^>]*\sheight=["\'](\d+)', svg_content)
    if w_match:
        width = int(w_match.group(1)) * scale
    if h_match:
        height = int(h_match.group(1)) * scale
    
    # Create image
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts
    try:
        font_normal = ImageFont.truetype('arial.ttf', int(14 * scale))
        font_small = ImageFont.truetype('arial.ttf', int(12 * scale))
    except:
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Parse rect elements
    rect_pattern = re.compile(r'<rect[^>]*>')
    for rect in re.finditer(r'<rect[^>]+>', svg_content):
        attrs = rect.group(0)
        
        x = y = w = h = 0
        fill = 'white'
        stroke = 'black'
        stroke_w = 1
        
        # Parse attributes
        for attr in re.finditer(r'(\w+)=["\']([^"\']*)["\']', attrs):
            key, val = attr.groups()
            if key == 'x':
                x = int(float(val)) * scale
            elif key == 'y':
                y = int(float(val)) * scale
            elif key in ('width', 'height'):
                if key == 'width':
                    w = int(float(val)) * scale
                else:
                    h = int(float(val)) * scale
            elif key == 'fill':
                fill = val
            elif key == 'stroke':
                stroke = val
        
        if w > 0 and h > 0:
            draw.rectangle([x, y, x + w, y + h], 
                          outline=parse_color(stroke),
                          fill=parse_color(fill) if fill != 'none' else None,
                          width=int(stroke_w * scale))
    
    # Parse line elements
    for line in re.finditer(r'<line[^>]+/>', svg_content):
        attrs = line.group(0)
        
        x1 = y1 = x2 = y2 = 0
        stroke = 'black'
        
        for attr in re.finditer(r'(\w+)=["\']([^"\']*)["\']', attrs):
            key, val = attr.groups()
            if key == 'x1':
                x1 = int(float(val)) * scale
            elif key == 'y1':
                y1 = int(float(val)) * scale
            elif key == 'x2':
                x2 = int(float(val)) * scale
            elif key == 'y2':
                y2 = int(float(val)) * scale
            elif key == 'stroke':
                stroke = val
        
        if x1 != x2 or y1 != y2:
            draw.line([x1, y1, x2, y2], fill=parse_color(stroke), width=int(scale))
    
    # Parse text elements
    for text in re.finditer(r'<text[^>]*>([^<]*)</text>', svg_content):
        content = text.group(1)
        
        # Find position
        text_tag = text.group(0)
        x = y = 0
        font_size = 14
        
        for attr in re.finditer(r'(\w+)=["\']([^"\']*)["\']', text_tag):
            key, val = attr.groups()
            if key == 'x':
                x = int(float(val)) * scale
            elif key == 'y':
                y = int(float(val)) * scale
            elif key == 'font-size':
                font_size = int(float(val)) * scale
        
        if x > 0 and y > 0:
            try:
                font = ImageFont.truetype('arial.ttf', font_size)
            except:
                font = font_normal
            
            draw.text((x, y - font_size), content, fill='black', font=font)
    
    # Save
    if png_path is None:
        png_path = os.path.splitext(svg_path)[0] + '.png'
    
    img.save(png_path)
    print(f'Saved: {png_path}')
    return png_path


def main():
    parser = argparse.ArgumentParser(description='Конвертер SVG в PNG')
    parser.add_argument('input', help='Входной SVG файл')
    parser.add_argument('output', nargs='?', help='Выходной PNG файл')
    parser.add_argument('--scale', type=int, default=1, help='Масштаб (по умолчанию: 1)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f'Error: File not found: {args.input}', file=sys.stderr)
        sys.exit(1)
    
    svg_to_png(args.input, args.output, args.scale)


if __name__ == '__main__':
    main()