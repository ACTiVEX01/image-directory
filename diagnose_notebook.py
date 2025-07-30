#!/usr/bin/env python3
"""
Diagnostic tool for Jupyter notebook files
This script helps identify common issues with .ipynb files
"""

import json
import sys
import nbformat

def diagnose_notebook(file_path):
    """Diagnose common issues with a notebook file"""
    print(f"Diagnosing: {file_path}")
    print("-" * 50)
    
    # Check if file exists
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ File not found")
        return False
    except Exception as e:
        print(f"❌ Cannot read file: {e}")
        return False
    
    # Check if it's valid JSON
    try:
        data = json.loads(content)
        print("✅ Valid JSON format")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        print("💡 Your file is not a valid JSON format. Please check for:")
        print("   - Missing quotes around strings")
        print("   - Trailing commas")
        print("   - Unclosed brackets or braces")
        return False
    
    # Check if it has required notebook fields
    required_fields = ['cells', 'metadata', 'nbformat']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        print(f"❌ Missing required fields: {', '.join(missing_fields)}")
        print("💡 Your file doesn't appear to be a valid Jupyter notebook")
        return False
    else:
        print("✅ Has required notebook fields")
    
    # Check nbformat version
    nbformat_version = data.get('nbformat', 0)
    if nbformat_version < 4:
        print(f"⚠️  Old notebook format (v{nbformat_version}). Consider upgrading to v4.")
    else:
        print(f"✅ Notebook format version: {nbformat_version}")
    
    # Check cells
    cells = data.get('cells', [])
    if not cells:
        print("⚠️  Notebook has no cells")
    else:
        print(f"✅ Notebook has {len(cells)} cells")
        
        # Check cell types
        cell_types = {}
        for cell in cells:
            cell_type = cell.get('cell_type', 'unknown')
            cell_types[cell_type] = cell_types.get(cell_type, 0) + 1
        
        print(f"   Cell breakdown: {dict(cell_types)}")
    
    # Try to load with nbformat
    try:
        with open(file_path, 'r') as f:
            notebook = nbformat.read(f, as_version=4)
        print("✅ Successfully loaded with nbformat")
    except nbformat.ValidationError as e:
        print(f"❌ Notebook validation error: {e}")
        print("💡 Your notebook has structural issues. Try opening it in Jupyter and saving it again.")
        return False
    except Exception as e:
        print(f"❌ nbformat loading error: {e}")
        return False
    
    print("\n🎉 Your notebook appears to be valid for PDF conversion!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python diagnose_notebook.py <notebook_file.ipynb>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    diagnose_notebook(file_path)