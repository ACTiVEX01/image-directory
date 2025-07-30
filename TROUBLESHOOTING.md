# Troubleshooting Guide

If you're getting an "error occurred" message when uploading your .ipynb file, this guide will help you identify and fix the issue.

## 🔧 Quick Diagnosis

1. **Use the Diagnostic Tool**: Click the "Diagnose Issues" button instead of "Convert to PDF" to get detailed information about what's wrong with your notebook.

2. **Check the error message**: The application now provides specific error messages to help you understand the problem.

## 🚨 Common Issues and Solutions

### 1. Invalid JSON Format

**Error**: "Invalid JSON format" or "Notebook does not appear to be JSON"

**Cause**: Your .ipynb file has corrupted JSON structure.

**Solutions**:
- Open your notebook in Jupyter Notebook/JupyterLab
- Save it again (Ctrl+S or File > Save)
- This will fix most JSON formatting issues

### 2. File Encoding Issues

**Error**: "File encoding error" or "UnicodeDecodeError"

**Cause**: Your notebook file was saved with incorrect encoding.

**Solutions**:
- Open the notebook in a text editor and save it as UTF-8
- Or open in Jupyter and save again
- Avoid copying notebook content through applications that might change encoding

### 3. Missing Required Fields

**Error**: "Missing required notebook fields"

**Cause**: The file is not a valid Jupyter notebook.

**Solutions**:
- Make sure you're uploading an actual .ipynb file
- Check that the file wasn't corrupted during download/transfer
- Try creating a new notebook and copying your content over

### 4. Empty Notebook

**Error**: "Notebook appears to be empty"

**Cause**: Your notebook has no cells.

**Solutions**:
- Add some content to your notebook (markdown or code cells)
- Make sure you saved the notebook after adding content

### 5. LaTeX Conversion Errors

**Error**: "LaTeX conversion failed"

**Cause**: Complex mathematical formulas or unsupported LaTeX commands.

**Solutions**:
- Simplify complex mathematical expressions
- Remove unsupported LaTeX packages or commands
- Check that mathematical formulas use standard LaTeX syntax
- Try converting a simple version first

### 6. Large File Size

**Error**: "File too large" or upload fails

**Cause**: File exceeds 16MB limit.

**Solutions**:
- Remove large images or outputs from your notebook
- Clear all cell outputs: Cell > All Output > Clear
- Split large notebooks into smaller parts

### 7. Notebook Format Version Issues

**Error**: "Old notebook format"

**Cause**: Your notebook uses an older format version.

**Solutions**:
- Open in Jupyter Notebook/JupyterLab
- The system will automatically upgrade the format
- Save the notebook

## 🛠️ Step-by-Step Fix Process

1. **Backup your notebook**: Make a copy before making changes

2. **Open in Jupyter**: 
   ```bash
   jupyter notebook your_file.ipynb
   ```

3. **Check for errors**: Look for any red error messages in cells

4. **Clear outputs** (if file is large):
   - Menu: Cell > All Output > Clear

5. **Save the notebook**:
   - Ctrl+S or File > Save

6. **Try conversion again**

## 🔍 Manual Validation

You can also validate your notebook manually:

### Check JSON Structure
```bash
python -m json.tool your_notebook.ipynb > /dev/null
```
If this command gives an error, your JSON is invalid.

### Use nbformat validation
```python
import nbformat

# Try to read the notebook
with open('your_notebook.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)
print("Notebook is valid!")
```

## 🔧 Command Line Diagnostic Tool

You can also use the standalone diagnostic tool:

```bash
cd /workspace
source venv/bin/activate
python diagnose_notebook.py your_notebook.ipynb
```

This will give you detailed information about any issues.

## 📝 Creating a Test Notebook

If you're still having issues, try converting this minimal test notebook:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["# Test Notebook\n\nThis is a test."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": ["print('Hello, World!')"]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
```

Save this as `test.ipynb` and try converting it. If this works, the issue is with your original notebook.

## 🆘 Still Having Issues?

If none of these solutions work:

1. **Check the console**: Look for error messages in your browser's console (F12)

2. **Try a different browser**: Sometimes browser-specific issues can occur

3. **Simplify your notebook**: Remove complex elements one by one to identify the problematic content

4. **Check LaTeX installation**: The server needs LaTeX installed for PDF conversion

5. **File permissions**: Make sure your file isn't read-only or corrupted

## 💡 Prevention Tips

- Always save notebooks in Jupyter before exporting
- Regularly validate your notebooks if you edit them outside of Jupyter
- Keep backups of important notebooks
- Use standard markdown and LaTeX syntax
- Clear outputs before sharing notebooks to reduce file size

## 🔧 Server-Side Issues

If the server itself has issues:

- **LaTeX not installed**: Server needs TeXLive and pandoc
- **Python dependencies**: Make sure all required packages are installed
- **Disk space**: Server needs space for temporary file processing
- **Memory**: Large notebooks may require more memory

Contact your system administrator if you suspect server-side issues.