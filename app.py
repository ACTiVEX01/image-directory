import os
import tempfile
import uuid
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
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Create PDF exporter
        pdf_exporter = PDFExporter()
        pdf_exporter.template_name = 'classic'
        
        # Convert to PDF
        (body, resources) = pdf_exporter.from_notebook_node(notebook)
        
        # Write PDF file
        with open(output_path, 'wb') as f:
            f.write(body)
        
        return True, "Conversion successful"
    except Exception as e:
        return False, str(e)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)