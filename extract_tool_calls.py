#!/usr/bin/env python3
"""
Extract file contents from tool calls in the transcript.
"""
import json
import re
from pathlib import Path
from collections import OrderedDict

transcript_path = "/Users/prateeksrivastava-mac/.cursor/projects/Volumes-disc-2-coding-automation/agent-transcripts/d48509d2-5087-4b37-ae2a-b69c6fa6b7e7/d48509d2-5087-4b37-ae2a-b69c6fa6b7e7.jsonl"

# Track the most recent file contents (ordered by line number)
files = OrderedDict()

print("Parsing transcript for tool calls...")

with open(transcript_path, 'r') as f:
    lines = f.readlines()

total_lines = len(lines)
print(f"Total lines: {total_lines}")

# Parse from the end to get the most recent versions
for line_num in range(total_lines - 1, -1, -1):
    line = lines[line_num]
    try:
        entry = json.loads(line)
        
        # Look for tool calls
        if 'tool_calls' in entry:
            for tool_call in entry['tool_calls']:
                tool_name = tool_call.get('name')
                params = tool_call.get('parameters', {})
                
                if tool_name == 'Write':
                    path = params.get('path', '')
                    contents = params.get('contents', '')
                    
                    if path and contents:
                        filename = Path(path).name
                        # Only store if we haven't seen this file yet (most recent)
                        if filename not in files:
                            files[filename] = {
                                'path': path,
                                'contents': contents,
                                'line': line_num + 1
                            }
                            print(f"Found {filename} at line {line_num + 1}")
                
                elif tool_name == 'StrReplace':
                    path = params.get('path', '')
                    new_string = params.get('new_string', '')
                    
                    if path:
                        filename = Path(path).name
                        # Track replacements but don't overwrite full writes
                        if filename not in files:
                            print(f"Found replacement in {filename} at line {line_num + 1}")
    
    except (json.JSONDecodeError, KeyError):
        continue

print(f"\n\nFound {len(files)} complete files")

# Now read the files in order and save them
output_dir = Path("/Volumes/disc 2/coding/automation/recovered_files")
output_dir.mkdir(exist_ok=True)

print(f"\nSaving files to {output_dir}...")
for filename, data in files.items():
    output_path = output_dir / filename
    with open(output_path, 'w') as f:
        f.write(data['contents'])
    print(f"  Saved: {filename} (from line {data['line']})")

print("\n\nDone! Files saved to recovered_files/")
