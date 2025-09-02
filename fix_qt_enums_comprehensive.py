#!/usr/bin/env python3
"""
Comprehensive Qt enum fixer for macOS compatibility.
Fixes all Qt enum bitwise operations throughout the Lucas Chess codebase.
"""
import os
import re
import glob

def fix_qt_enums_in_file(file_path):
    """Fix Qt enum issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    original_content = content
    changes = []
    
    # Pattern 1: Simple bitwise operations with Qt enums
    # Example: QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop
    pattern1 = r'(QtCore\.Qt\.\w+|QtGui\.QPainter\.\w+|QtWidgets\.QGraphicsView\.\w+)\s*\|\s*(QtCore\.Qt\.\w+|QtGui\.QPainter\.\w+|QtWidgets\.QGraphicsView\.\w+)(\s*\|\s*(QtCore\.Qt\.\w+|QtGui\.QPainter\.\w+|QtWidgets\.QGraphicsView\.\w+))*'
    
    def replace_bitwise_ops(match):
        expr = match.group(0)
        # Split by | and wrap each part with int()
        parts = [part.strip() for part in expr.split('|')]
        int_parts = [f'int({part})' for part in parts]
        return ' | '.join(int_parts)
    
    new_content = re.sub(pattern1, replace_bitwise_ops, content)
    if new_content != content:
        changes.append("Fixed bitwise operations")
        content = new_content
    
    # Pattern 2: setWindowFlags patterns
    patterns = [
        (r'setWindowFlags\(\s*([^)]+)\s*\)', r'setWindowFlags(QtCore.Qt.WindowFlags(\1))'),
        (r'setRenderHints\(\s*([^)]+)\s*\)', r'setRenderHints(QtGui.QPainter.RenderHints(\1))'),
        (r'setAlignment\(\s*([^)]+)\s*\)', r'setAlignment(QtCore.Qt.Alignment(\1))'),
        (r'setTextInteractionFlags\(\s*([^)]+)\s*\)', r'setTextInteractionFlags(QtCore.Qt.TextInteractionFlags(\1))'),
    ]
    
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes.append(f"Fixed method calls: {pattern}")
            content = new_content
    
    # Only write if changes were made
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {file_path}: {', '.join(changes)}")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    return False

def main():
    """Fix Qt enums in all Python files in the Code directory"""
    print("Fixing Qt enum compatibility issues for macOS...")
    
    # Get all Python files in the Code directory
    code_dir = "bin/Code"
    if not os.path.exists(code_dir):
        print(f"Error: {code_dir} directory not found")
        return
    
    python_files = []
    for root, dirs, files in os.walk(code_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files to process")
    
    fixed_count = 0
    for file_path in python_files:
        if fix_qt_enums_in_file(file_path):
            fixed_count += 1
    
    print(f"Fixed Qt enum issues in {fixed_count} files")
    
    # Also fix the main files we know have issues
    other_files = [
        "bin/Code/MainWindow/MainWindow.py",
        "bin/Code/QT/LCDialog.py", 
        "bin/Code/Board/Board.py"
    ]
    
    for file_path in other_files:
        if os.path.exists(file_path):
            fix_qt_enums_in_file(file_path)

if __name__ == "__main__":
    main()