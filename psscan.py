import argparse
import urllib.request
import re
import sys

# Scans FASTA sequences for PROSITE-style sequence motifs.
# Patterns can be given directly or downloaded from the PROSITE database,
# then converted to regular expressions and reported with 1-based match positions.


# Reading arguments
parser = argparse.ArgumentParser(  
)
parser.add_argument(
    "--fasta",
    required=True
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--pattern")
group.add_argument("--web")

parser.add_argument(
    "--extern",
    action = "store_true"
)

args = parser.parse_args()

genome = {}

# FASTA reader, works with both stdin and a FASTA file

if args.fasta == "-":
    lines = sys.stdin.readlines()
else:
    with open(args.fasta) as f:
        lines = f.readlines()

current_id = ""
current_chunk = []
genome = {}

for line in lines:
    line = line.strip()
    if line.startswith(">"):
         if current_id != "":
             genome[current_id] = "".join(current_chunk)
             
         current_id = line[1:].strip()
         current_chunk = []
    else:
        if current_id == "":
            raise ValueError("ERROR 1 reading the fasta: starting with sequence ")
        current_chunk.append(line)
    
if current_id != "":
    genome[current_id] = "".join(current_chunk)


# Fetching pattern form the web

prosite_id = args.web

if args.web:
    url = f"https://prosite.expasy.org/{prosite_id}.txt"

    with urllib.request.urlopen(url) as response:
        entry = response.read().decode("utf-8")

    pattern = None
    for line in entry.splitlines():
        if line.startswith("PA"):
            pattern = line[5:].rstrip(".").strip()
            break
else:
    pattern = args.pattern
    
    
# Translating to regex
    
mapToRegex= {
    "x" : ".",
    "(" : "{",
    ")" : "}",
    "{" : "[^",
    "}" : "]",
    "-" : "",
    "<" : "^",
    ">" : "$"

}


regex= ""

for char in pattern:
    if char not in mapToRegex:
        regex += char
    else:
        regex += mapToRegex[char]
        

overlap_regex = f"(?=({regex}))" #lookahead(dont consume)

for key in genome.keys():
    for match in re.finditer(overlap_regex, genome[key]):
        start_pos = match.start() + 1
        print(f"{key}\t{start_pos}\t{match.group(1)}")
        
   
    