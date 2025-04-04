#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path

class NameNormalizer:
    def __init__(self, config):
        self.config = config
        self.changes = []
    
    def normalize(self, name):
        original = name
        if self.config['lowercase']:
            name = name.lower()
        if self.config['replace_special']:
            pattern = r'[^\w\-\.]' if self.config['keep_underscore'] else r'[^\w\.]'
            name = re.sub(pattern, self.config['replacement_char'], name)
        return name

    def record_change(self, old, new, level):
        self.changes.append((level, old, new))

def print_tree(changes):
    print("\n" + "="*40 + "\nFile System Changes Tree:\n" + "="*40)
    current_level = 0
    
    for level, old, new in sorted(changes, key=lambda x: x[0]):
        indent = "    " * level
        if old == new:
            print(f"{indent}├── [UNCHANGED] {old}")
        else:
            print(f"{indent}├── {old}")
            print(f"{indent}|   └──>> {new}")
    print("="*40 + "\n")

def process_path(root, path, normalizer, dry_run, level=0):
    old_path = Path(root) / path
    new_name = normalizer.normalize(path)
    new_path = Path(root) / new_name
    
    # Handle duplicates
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
    parser.add_argument('-r', '--replace-special', action='store_true', help="Replace special chars")
    parser.add_argument('-c', '--replacement-char', default='-', help="Replacement character")
    parser.add_argument('-k', '--keep-underscore', action='store_true', help="Preserve underscores")
    parser.add_argument('-p', '--path', default='.', help="Target path")
    parser.add_argument('-d', '--dry-run', action='store_true', help="Preview changes")
    parser.add_argument('-v', '--verbose', action='store_true', help="Show full paths")
    
    args = parser.parse_args()
    normalizer = NameNormalizer(vars(args))
    
    # Process files
    for root, dirs, files in os.walk(args.path, topdown=True):
        level = root.replace(args.path, '').count(os.sep)
        
        # Process directories first (top-down)
        for name in dirs[:]:  # Copy for modification during walk
            process_path(root, name, normalizer, args.dry_run, level)
        
        # Then process files
        for name in files:
            process_path(root, name, normalizer, args.dry_run, level+1)
    
    # Display results
    if args.verbose:
        for level, old, new in normalizer.changes:
            full_old = str(Path(root) / old)
            full_new = str(Path(root) / new)
            print(f"{'  '*level}{full_old} → {full_new}")
    else:
        print_tree(normalizer.changes)
    
    # Summary
    changed = sum(1 for _, old, new in normalizer.changes if old != new)
    print(f"\nSummary: {changed} changes {'(dry run)' if args.dry_run else ''}")

if __name__ == "__main__":
    main()