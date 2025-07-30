# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-30

### Added
- Initial release of Jupyter Notebook to PDF Converter
- Web-based interface with drag-and-drop file upload
- PDF conversion using nbconvert and LaTeX
- Beautiful, modern UI with gradient design
- Progress indicators and loading animations
- File validation and error handling
- Automatic file cleanup after download
- Mobile-responsive design
- Support for markdown cells, code cells, and mathematical formulas

### Features
- **File Upload**: Drag-and-drop or click to upload .ipynb files
- **PDF Conversion**: High-quality PDF output using LaTeX backend
- **Error Handling**: Comprehensive error messages and validation
- **File Management**: Automatic cleanup with unique file naming
- **Security**: File type validation and size limits (16MB)
- **UI/UX**: Modern design with hover effects and animations

### Technical
- Flask backend with RESTful API endpoints
- nbconvert integration for reliable conversion
- LaTeX and pandoc support for mathematical expressions
- Temporary file handling with UUID-based naming
- JSON validation for notebook files

## [1.1.0] - 2025-01-30

### Added
- **Diagnostic Tool**: New "Diagnose Issues" button for troubleshooting
- **Enhanced Error Handling**: Detailed, specific error messages
- **Command-line Diagnostic**: Standalone `diagnose_notebook.py` tool
- **Comprehensive Documentation**: TROUBLESHOOTING.md guide
- **Better Validation**: Multi-stage notebook validation process

### Improved
- **Error Messages**: Specific feedback for different error types
- **User Experience**: Clear guidance on fixing common issues
- **File Validation**: Better detection of JSON and notebook format issues
- **LaTeX Error Handling**: Specific messages for LaTeX conversion problems

### Fixed
- **JSON Parsing**: Better handling of malformed notebook files
- **Encoding Issues**: Improved UTF-8 encoding detection
- **Empty Notebooks**: Clear messaging for notebooks without cells
- **Large Files**: Better handling of oversized uploads

### Technical
- Enhanced `convert_notebook_to_pdf()` function with granular error handling
- New `/diagnose` API endpoint for file analysis
- Improved frontend with dual-button interface
- Better error categorization and user feedback

### Documentation
- Added TROUBLESHOOTING.md with comprehensive solutions
- Updated README.md with diagnostic features
- Created CONTRIBUTING.md for development guidelines
- Added CHANGELOG.md for version tracking

---

## Version History

### v1.1.0 - Enhanced Diagnostics (Current)
- Added diagnostic tool and improved error handling
- Comprehensive troubleshooting documentation
- Better user experience with specific error messages

### v1.0.0 - Initial Release
- Basic notebook to PDF conversion functionality
- Web interface with file upload
- PDF generation using nbconvert and LaTeX

---

## Upcoming Features

### Planned for v1.2.0
- [ ] Batch conversion support
- [ ] Additional export formats (HTML, Word)
- [ ] Improved mobile interface
- [ ] Configuration options for PDF output
- [ ] Better LaTeX template selection

### Under Consideration
- [ ] Cloud storage integration
- [ ] API rate limiting
- [ ] User authentication
- [ ] Conversion history
- [ ] Advanced formatting options

---

## Breaking Changes

### v1.1.0
- No breaking changes, fully backward compatible

### v1.0.0
- Initial release, no previous versions

---

## Migration Guide

### From v1.0.0 to v1.1.0
No migration needed. All existing functionality remains the same with enhanced features added.

---

## Contributors

Special thanks to all contributors who have helped improve this project:

- Initial development and core features
- Diagnostic tools and error handling improvements
- Documentation and troubleshooting guides
- Testing and bug reports

---

## Support

For questions, issues, or contributions:
- **Issues**: [GitHub Issues](https://github.com/yourusername/jupyter-notebook-to-pdf/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jupyter-notebook-to-pdf/discussions)
- **Documentation**: README.md and TROUBLESHOOTING.md