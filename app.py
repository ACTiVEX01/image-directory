import os
import tempfile
import uuid
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import nbformat
from nbconvert import PDFExporter
from nbconvert.writers import FilesWriter
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'ipynb'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_notebook_to_pdf(notebook_path, output_path):
    """Convert a Jupyter notebook to PDF using nbconvert"""
    try:
        # Read and validate the notebook
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)
        except nbformat.ValidationError as e:
            return False, f"Invalid notebook format: {str(e)}"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON in notebook file: {str(e)}"
        except UnicodeDecodeError as e:
            return False, f"File encoding error: {str(e)}"
        
        # Validate notebook structure
        if not notebook.cells:
            return False, "Notebook appears to be empty (no cells found)"
        
        # Create PDF exporter with better configuration
        try:
            pdf_exporter = PDFExporter()
            pdf_exporter.template_name = 'classic'
            
            # Configure the exporter to handle common issues
            pdf_exporter.exclude_input_prompt = False
            pdf_exporter.exclude_output_prompt = False
            
        except Exception as e:
            return False, f"Failed to initialize PDF exporter: {str(e)}"
        
        # Convert to PDF
        try:
            (body, resources) = pdf_exporter.from_notebook_node(notebook)
        except Exception as e:
            if "xelatex" in str(e).lower() or "latex" in str(e).lower():
                return False, "LaTeX conversion failed. Please ensure your notebook doesn't contain unsupported LaTeX commands or complex formatting."
            elif "pandoc" in str(e).lower():
                return False, "Pandoc conversion error. Please check if pandoc is properly installed."
            else:
                return False, f"Notebook conversion failed: {str(e)}"
        
        # Write PDF file
        try:
            with open(output_path, 'wb') as f:
                f.write(body)
        except Exception as e:
            return False, f"Failed to write PDF file: {str(e)}"
        
        return True, "Conversion successful"
        
    except Exception as e:
        return False, f"Unexpected error during conversion: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.ipynb'):
        return jsonify({'error': 'Invalid file type. Please upload a .ipynb file.'}), 400
        
    if file and allowed_file(file.filename):
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Save uploaded file
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        file.save(upload_path)
        
        # Convert to PDF
        output_filename = f"{unique_id}_{name_without_ext}.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        success, message = convert_notebook_to_pdf(upload_path, output_path)
        
        if success:
            # Clean up uploaded file
            os.remove(upload_path)
            
            return jsonify({
                'success': True,
                'message': 'File converted successfully',
                'download_id': unique_id,
                'original_filename': name_without_ext,
                'output_filename': output_filename
            })
        else:
            # Clean up uploaded file
            if os.path.exists(upload_path):
                os.remove(upload_path)
            
            return jsonify({
                'success': False,
                'error': f'Conversion failed: {message}'
            }), 500
    
    return jsonify({'error': 'Invalid file type. Please upload a .ipynb file.'}), 400

@app.route('/download/<download_id>/<filename>')
def download_file(download_id, filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        def remove_file():
            try:
                os.remove(file_path)
            except:
                pass
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup/<download_id>/<filename>', methods=['DELETE'])
def cleanup_file(download_id, filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/diagnose', methods=['POST'])
def diagnose_file():
    """Diagnose issues with uploaded notebook files"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.ipynb'):
        return jsonify({'error': 'Please upload a .ipynb file for diagnosis'}), 400
    
    # Save temporary file for diagnosis
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_diagnose_{file.filename}")
    file.save(temp_path)
    
    try:
        issues = []
        suggestions = []
        
        # Read file content
        try:
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            issues.append("File encoding issue - file is not valid UTF-8")
            suggestions.append("Save your notebook with UTF-8 encoding")
            return jsonify({
                'valid': False,
                'issues': issues,
                'suggestions': suggestions
            })
        
        # Check JSON validity
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            issues.append(f"Invalid JSON format: {str(e)}")
            suggestions.append("Open your notebook in Jupyter and save it again to fix JSON formatting")
            return jsonify({
                'valid': False,
                'issues': issues,
                'suggestions': suggestions
            })
        
        # Check required fields
        required_fields = ['cells', 'metadata', 'nbformat']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            issues.append(f"Missing required notebook fields: {', '.join(missing_fields)}")
            suggestions.append("This doesn't appear to be a valid Jupyter notebook file")
            return jsonify({
                'valid': False,
                'issues': issues,
                'suggestions': suggestions
            })
        
        # Check cells
        cells = data.get('cells', [])
        if not cells:
            issues.append("Notebook has no cells")
            suggestions.append("Add some content to your notebook before converting")
        
        # Try nbformat validation
        try:
            with open(temp_path, 'r') as f:
                notebook = nbformat.read(f, as_version=4)
        except nbformat.ValidationError as e:
            issues.append(f"Notebook validation error: {str(e)}")
            suggestions.append("Open your notebook in Jupyter, check for errors, and save it again")
            return jsonify({
                'valid': False,
                'issues': issues,
                'suggestions': suggestions
            })
        
        # If we get here, the notebook is valid
        cell_count = len(cells)
        cell_types = {}
        for cell in cells:
            cell_type = cell.get('cell_type', 'unknown')
            cell_types[cell_type] = cell_types.get(cell_type, 0) + 1
        
        return jsonify({
            'valid': True,
            'info': {
                'cell_count': cell_count,
                'cell_types': cell_types,
                'nbformat_version': data.get('nbformat', 'unknown')
            },
            'message': 'Your notebook looks good for PDF conversion!'
        })
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)