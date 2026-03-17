#!/usr/bin/env python3
"""
Extract the most recent complete file contents from the conversation transcript.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

transcript_path = "/Users/prateeksrivastava-mac/.cursor/projects/Volumes-disc-2-coding-automation/agent-transcripts/d48509d2-5087-4b37-ae2a-b69c6fa6b7e7/d48509d2-5087-4b37-ae2a-b69c6fa6b7e7.jsonl"

# Track the most recent complete file contents
file_contents = {}
file_line_numbers = {}

print("Parsing transcript...")

with open(transcript_path, 'r') as f:
    for line_num, line in enumerate(f, 1):
        try:
            entry = json.loads(line)
            if entry.get('role') != 'assistant':
                continue
            
            message = entry.get('message', {})
            content = message.get('content', [])
            
            for item in content:
                if item.get('type') != 'text':
                    continue
                
                text = item.get('text', '')
                
                # Look for file write patterns
                # Pattern 1: Write tool calls (look for file paths and code blocks)
                write_pattern = r'(?:Write|StrReplace|creating?|updating?)\s+[`"]?([^`"\n]+\.(?:py|env|sh|md))[`"]?'
                matches = re.finditer(write_pattern, text, re.IGNORECASE)
                
                for match in matches:
                    filepath = match.group(1)
                    
                    # Extract code blocks after the file mention
                    code_blocks = re.findall(r'```(?:python|bash|env)?\n(.*?)```', text[match.end():], re.DOTALL)
                    
                    if code_blocks:
                        # Store the most recent version
                        file_contents[filepath] = code_blocks[0].strip()
                        file_line_numbers[filepath] = line_num
                        print(f"Found {filepath} at line {line_num}")
        
        except json.JSONDecodeError:
            continue

print(f"\n\nFound {len(file_contents)} files:")
for filepath in sorted(file_contents.keys()):
    print(f"  - {filepath} (line {file_line_numbers[filepath]})")

# Save the extracted files
output_dir = Path("/Volumes/disc 2/coding/automation/recovered_files")
output_dir.mkdir(exist_ok=True)

print(f"\n\nSaving files to {output_dir}...")
for filepath, content in file_contents.items():
    filename = Path(filepath).name
    output_path = output_dir / filename
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"  Saved: {filename}")

print("\n\nDone!")
