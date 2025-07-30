# Contributing to Jupyter Notebook to PDF Converter

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use the issue template** if available
3. **Provide detailed information**:
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Error messages (if any)
   - System information (OS, Python version, etc.)
   - Sample notebook file (if relevant)

### Suggesting Features

1. **Open an issue** to discuss the feature first
2. **Explain the use case** and why it would be valuable
3. **Consider backwards compatibility**

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**
4. **Test your changes thoroughly**
5. **Follow the coding standards**
6. **Commit with clear messages**
7. **Submit a pull request**

## Development Setup

1. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/jupyter-notebook-to-pdf.git
   cd jupyter-notebook-to-pdf
   ```

2. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install LaTeX** (for PDF conversion):
   - Ubuntu/Debian: `sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic pandoc`
   - macOS: `brew install --cask mactex` or `brew install basictex`
   - Windows: Install MiKTeX from https://miktex.org/download

## Coding Standards

### Python Code
- Follow **PEP 8** style guidelines
- Use **meaningful variable names**
- Add **docstrings** for functions and classes
- Include **type hints** where appropriate
- Keep functions **small and focused**

### Frontend Code
- Use **semantic HTML**
- Follow **consistent naming conventions**
- Add **comments** for complex logic
- Ensure **accessibility** (ARIA labels, keyboard navigation)
- Test on **multiple browsers**

### Documentation
- Update **README.md** if adding new features
- Update **TROUBLESHOOTING.md** for new error cases
- Use **clear, concise language**
- Include **code examples** where helpful

## Testing

### Before Submitting
1. **Test with various notebook types**:
   - Simple notebooks (markdown + code)
   - Notebooks with mathematical formulas
   - Large notebooks
   - Notebooks with images
   - Empty notebooks
   - Invalid notebooks

2. **Test error handling**:
   - Upload invalid files
   - Test with corrupted notebooks
   - Test file size limits

3. **Test the diagnostic tool**:
   - Verify it correctly identifies issues
   - Check that suggestions are helpful

### Manual Testing Checklist
- [ ] File upload works (drag & drop and click)
- [ ] Conversion produces valid PDF
- [ ] Diagnostic tool identifies issues correctly
- [ ] Error messages are helpful
- [ ] File cleanup works properly
- [ ] Download function works
- [ ] UI is responsive on mobile

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update version numbers** if applicable
5. **Squash commits** if requested
6. **Respond to review feedback** promptly

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] Tested with various notebook types
- [ ] Tested error handling
- [ ] Tested on multiple browsers
- [ ] All existing tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed the code
- [ ] Added comments for complex code
- [ ] Updated documentation
- [ ] No new warnings introduced
```

## Areas for Contribution

### High Priority
- **Performance improvements** for large notebooks
- **Better error messages** and user guidance
- **Additional export formats** (HTML, Word, etc.)
- **Batch conversion** support
- **API improvements**

### Medium Priority
- **UI/UX improvements**
- **Mobile optimization**
- **Accessibility enhancements**
- **Internationalization**
- **Configuration options**

### Low Priority
- **Themes and customization**
- **Advanced LaTeX features**
- **Integration with cloud storage**
- **Command-line interface**

## Code of Conduct

### Our Standards
- **Be respectful** and inclusive
- **Welcome newcomers** and help them learn
- **Focus on constructive feedback**
- **Respect different viewpoints** and experiences

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or inflammatory comments
- Personal attacks
- Publishing private information

## Getting Help

- **Documentation**: Check README.md and TROUBLESHOOTING.md
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: Ask for help in your pull request

## Recognition

Contributors will be acknowledged in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for helping make this project better! 🚀