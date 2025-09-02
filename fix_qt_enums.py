#!/usr/bin/env python3
"""
Script to automatically fix Qt enum bitwise operations for macOS compatibility.
This converts all Qt enum | operations to int-based operations.
"""

import os
import re
import sys

def fix_qt_enums_in_file(filepath):
    """Fix Qt enum bitwise operations in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match Qt enum | enum operations
        patterns = [
            # QtCore.Qt.Something | QtCore.Qt.SomethingElse
            (r'(QtCore\.Qt\.\w+)\s*\|\s*(QtCore\.Qt\.\w+)', r'int(\1) | int(\2)'),
            # Qt.Something | Qt.SomethingElse  
            (r'\b(Qt\.\w+)\s*\|\s*(Qt\.\w+)', r'int(\1) | int(\2)'),
            # Handle chained operations like A | B | C
            (r'int\((QtCore\.Qt\.\w+)\) \| int\((QtCore\.Qt\.\w+)\)\s*\|\s*(QtCore\.Qt\.\w+)', 
             r'int(\1) | int(\2) | int(\3)'),
            (r'int\((Qt\.\w+)\) \| int\((Qt\.\w+)\)\s*\|\s*(Qt\.\w+)', 
             r'int(\1) | int(\2) | int(\3)'),
        ]
        
        # Apply patterns
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
            
        # Handle |= operations with Qt enums
        content = re.sub(r'(\w+)\s*\|\=\s*(QtCore\.Qt\.\w+)', r'\1 |= int(\2)', content)
        content = re.sub(r'(\w+)\s*\|\=\s*(Qt\.\w+)', r'\1 |= int(\2)', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Fix Qt enums in all Python files"""
    base_dir = "/Volumes/Mini-Ext/mini-external/Development/Lucas/lucaschessR2/bin/Code"
    fixed_files = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_qt_enums_in_file(filepath):
                    fixed_files.append(filepath)
    
    print(f"Fixed {len(fixed_files)} files:")
    for f in fixed_files:
        print(f"  {f}")

if __name__ == "__main__":
    main()