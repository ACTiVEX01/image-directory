# Jupyter Notebook to PDF Converter

A beautiful web application that converts Jupyter notebook (.ipynb) files to PDF format. Simply upload your notebook file and download the converted PDF instantly.

## Features

- 📁 **Drag & Drop Upload**: Easy file upload with drag and drop support
- ⚡ **Fast Conversion**: Quick conversion using nbconvert
- 🎨 **Beautiful UI**: Modern, responsive design with progress indicators
- 🔒 **Secure**: Files are automatically cleaned up after download
- 📱 **Mobile Friendly**: Works on desktop and mobile devices
- 💾 **No Storage**: Files are processed and removed immediately

## Prerequisites

- Python 3.7 or higher
- LaTeX distribution (for PDF conversion)

### Installing LaTeX

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic
```

#### macOS:
```bash
brew install --cask mactex
# or
brew install basictex
```

#### Windows:
Download and install MiKTeX from: https://miktex.org/download

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify LaTeX installation:**
```bash
pdflatex --version
```

## Usage

1. **Start the application:**
```bash
python app.py
```

2. **Open your web browser and navigate to:**
```
http://localhost:5000
```

3. **Upload and convert:**
   - Click the upload area or drag and drop your .ipynb file
   - Click "Convert to PDF" to convert, or "Diagnose Issues" to check for problems
   - Wait for the conversion to complete
   - Download your PDF file

4. **If you get an error:**
   - Use the "Diagnose Issues" button to get detailed information
   - See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common solutions

## Project Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Frontend interface
├── uploads/           # Temporary upload directory (auto-created)
└── outputs/           # Temporary output directory (auto-created)
```

## How It Works

1. **Upload**: User uploads a .ipynb file through the web interface
2. **Validation**: File is validated to ensure it's a valid notebook
3. **Conversion**: nbconvert processes the notebook and generates PDF
4. **Download**: User downloads the converted PDF file
5. **Cleanup**: Files are automatically removed after download

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload and convert notebook file
- `GET /download/<id>/<filename>` - Download converted PDF
- `DELETE /cleanup/<id>/<filename>` - Clean up files

## Configuration

You can modify these settings in `app.py`:

- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)
- `UPLOAD_FOLDER`: Directory for temporary uploads
- `OUTPUT_FOLDER`: Directory for converted files

## Troubleshooting

### Common Issues

1. **LaTeX not found error:**
   - Make sure LaTeX is installed and in your PATH
   - Try: `which pdflatex` (Unix) or `where pdflatex` (Windows)

2. **Conversion fails:**
   - Check if the notebook file is valid JSON
   - Ensure all required libraries are installed
   - Check the console for detailed error messages

3. **Large files fail to upload:**
   - Check the `MAX_CONTENT_LENGTH` setting
   - Ensure your notebook doesn't exceed the size limit

### Error Messages

- **"Invalid file type"**: Only .ipynb files are accepted
- **"File not found"**: The requested file may have been cleaned up
- **"Conversion failed"**: Usually indicates a LaTeX or notebook parsing issue

## Dependencies

- **Flask**: Web framework
- **nbconvert**: Jupyter notebook conversion
- **nbformat**: Notebook format handling
- **LaTeX**: PDF generation backend

## Security Notes

- Files are stored temporarily and cleaned up automatically
- Unique IDs prevent file name conflicts
- File type validation prevents malicious uploads
- No permanent storage of user files

## Browser Support

- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.