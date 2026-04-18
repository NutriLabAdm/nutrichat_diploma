#!/usr/bin/env python3
import base64, zlib, requests

test = """@startuml
left to right direction
entity "USERS" {
  *id
  name
}
USERS }|--|| PROFILES
@enduml"""

# Try different encodings
print("=== Test 1: Standard DEFLATE with ~1 ===")
compressed = zlib.compress(('-' + test).encode('utf-8'), 9)
encoded1 = base64.b64encode(compressed).decode().replace('+', '-').replace('/', '_').replace('=', '')
print(f"~1{encoded1[:50]}...")

r = requests.get(f"https://www.plantuml.com/plantuml/svg/~1{encoded1}", timeout=30)
print(f"Status: {r.status_code}, Contains SVG: {'<svg' in r.text[:50]}")

print("\n=== Test 2: Without leading dash ===")
compressed2 = zlib.compress(test.encode('utf-8'), 9)
encoded2 = base64.b64encode(compressed2).decode().replace('+', '-').replace('/', '_').replace('=', '')
print(f"~1{encoded2[:50]}...")

r2 = requests.get(f"https://www.plantuml.com/plantuml/svg/~1{encoded2}", timeout=30)
print(f"Status: {r2.status_code}, Contains SVG: {'<svg' in r2.text[:50]}")

print("\n=== Test 3: Direct (no ~1) ===")
r3 = requests.get(f"https://www.plantuml.com/plantuml/svg/{encoded2}", timeout=30)
print(f"Status: {r3.status_code}, Contains SVG: {'<svg' in r3.text[:50]}")