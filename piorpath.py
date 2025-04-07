#!/usr/bin/env python3
__version__ = "1.0.0"  # Update this with each release
import os
import re
import argparse
from pathlib import Path

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

class NameNormalizer:
    def __init__(self, config):
        self.config = config
        self.changes = []
    
    def normalize(self, name):
        original = name
        if not self.config['keep_spaces']:
            name = name.replace(' ', '')
        if self.config['lowercase']:
            name = name.lower()
        if self.config['replace_special']:
            pattern = r'[^a-zA-Z0-9_\-\. ]' if self.config['keep_spaces'] else r'[^a-zA-Z0-9_\-\.]'
        
        if self.config['replace_underscore']:
                pattern = r'[^a-zA-Z0-9\-\. ]' if self.config['keep_spaces'] else r'[^a-zA-Z0-9\-\.]'
        
        if self.config['replace_dashes']:
            if self.config['replace_underscore']:
                pattern = r'[^a-zA-Z0-9\. ]' if self.config['keep_spaces'] else r'[^a-zA-Z0-9\.]'
            else:
                pattern = r'[^a-zA-Z0-9_\. ]' if self.config['keep_spaces'] else r'[^a-zA-Z0-9_\.]'
            
        name = re.sub(pattern, self.config['replacement_char'], name)
        return name

    def record_change(self, old, new, level):
        self.changes.append((level, old, new))

def print_tree(changes):
    print("\n" + RED + "="*40 + RESET)
    print(RED + "File System Changes Tree:" + RESET)
    print(RED + "="*40 + RESET)
    
    for level, old, new in sorted(changes, key=lambda x: x[0]):
        indent = "    " * level
        if old == new:
            print(f"{indent}{GREEN}├──{RED}[UNCHANGED] {RESET}{old}")
        else:
            print(f"{indent}{GREEN}├──{RED} {RESET}{old}")
            print(f"{indent}{GREEN}|   {GREEN}└──>>{GREEN}{ RESET}{new}")
    print(RED + "="*40 + RESET + "\n")

def process_path(root, path, normalizer, dry_run, level=0):
    old_path = Path(root) / path
    new_name = normalizer.normalize(path)
    new_path = Path(root) / new_name
    
    counter = 1
    while new_path.exists() and new_path != old_path:
        stem, suffix = new_path.stem, new_path.suffix
        new_path = new_path.with_name(f"{stem}-{counter}{suffix}")
        counter += 1
    
    normalizer.record_change(path, new_name, level)
    
    if not dry_run and new_path != old_path:
        try:
            old_path.rename(new_path)
        except Exception as e:
            print(f"! Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Make your Paths great again!", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-l', '--lowercase', action='store_true', help="Convert to lowercase")
    parser.add_argument('-s', '--replace-special', action='store_true', help="Replace special chars")
    parser.add_argument('-c', '--replacement-char', default='', help="Replacement character")
    parser.add_argument('-u', '--replace-underscore', action='store_true', 
                        help="Replace underscores with replacement char")
    parser.add_argument('-d', '--replace-dashes', action='store_true', 
                        help="Replace dashes with replacement char")
    parser.add_argument('-k', '--keep-spaces', action='store_true',
                        help="Keep spaces in filenames (default: remove spaces)")
    parser.add_argument('-i', '--include-hidden', action='store_true',
                        help="Process hidden files/directories (default: skip)")
    parser.add_argument('-p', '--path', default='.', help="Target path")
    parser.add_argument('-dr', '--dry-run', action='store_true', help="Preview changes")
    parser.add_argument('-v', '--verbose', action='store_true', help="Show full paths")
    
    args = parser.parse_args()
    normalizer = NameNormalizer(vars(args))
    
    for root, dirs, files in os.walk(args.path, topdown=True):
        # Only filter hidden dirs if not including hidden files
        if not args.include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        level = root.replace(args.path, '').count(os.sep)
        
        for name in dirs[:]: 
            process_path(root, name, normalizer, args.dry_run, level)
        
        for name in files:
            if args.include_hidden or not name.startswith('.'):
                process_path(root, name, normalizer, args.dry_run, level+1)
    
    if args.verbose:
        for level, old, new in normalizer.changes:
            full_old = str(Path(root) / old)
            full_new = str(Path(root) / new)
            print(f"{RED}{'  '*level}{full_old} {RESET}→ {GREEN}{full_new}{RESET}")
    else:
        print_tree(normalizer.changes)
        
    changed = sum(1 for _, old, new in normalizer.changes if old != new)
    print(f"\nSummary: {changed} changes {'(dry run)' if args.dry_run else ''}")

if __name__ == "__main__":
    main()