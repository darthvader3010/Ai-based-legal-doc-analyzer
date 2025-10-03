# Quick Start Guide

Get started with the AI Legal Document Analyzer in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Quick Installation

### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
setup.bat
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_analyzer.py -v
```

### Option 3: Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## First Steps

### 1. Web Interface (Easiest)

```bash
python app.py
```

Then open your browser to: http://localhost:5000

**Features:**
- Drag and drop documents
- View analysis results instantly
- Search for keywords
- Beautiful, intuitive interface

### 2. Command Line

**Analyze a document:**
```bash
python cli.py analyze path/to/document.pdf
```

**Search for keywords:**
```bash
python cli.py search document.pdf --keywords "liability,warranty,termination"
```

**Export to JSON:**
```bash
python cli.py analyze document.pdf --json results.json
```

### 3. Python API

```python
from legal_analyzer import LegalDocumentAnalyzer

# Initialize
analyzer = LegalDocumentAnalyzer()

# Analyze document
results = analyzer.analyze_document('contract.pdf')

# Access results
print(f"Summary: {results['summary']}")
print(f"Clauses: {len(results['clauses'])}")
print(f"Definitions: {len(results['definitions'])}")
print(f"Obligations: {len(results['obligations'])}")

# Search keywords
search = analyzer.search_document('contract.pdf', ['liability', 'warranty'])
print(f"Matches: {search['total_matches']}")
```

## Example Workflow

1. **Upload Document**: Place your PDF, DOCX, or TXT file in a convenient location

2. **Analyze**: Run the analyzer to extract key information
   ```bash
   python cli.py analyze my-contract.pdf
   ```

3. **Review Results**: Check the summary, clauses, definitions, and obligations

4. **Search Keywords**: Find specific terms
   ```bash
   python cli.py search my-contract.pdf --keywords "indemnification,liability"
   ```

5. **Export**: Save results for later
   ```bash
   python cli.py analyze my-contract.pdf --json analysis.json
   ```

## Supported Document Types

- ✅ PDF files
- ✅ Microsoft Word (.docx)
- ✅ Plain text (.txt)

## What Gets Analyzed?

The analyzer extracts:

1. **Summary**: Concise overview of the document
2. **Clauses**: Numbered sections and subsections
3. **Definitions**: Key terms and their meanings
4. **Obligations**: Legal requirements and duties
5. **Key Points**: Critical actionable items

## Common Issues

**Problem:** `ModuleNotFoundError`
- **Solution:** Run `pip install -r requirements.txt`

**Problem:** "File not found"
- **Solution:** Check file path and permissions

**Problem:** Port 5000 already in use
- **Solution:** Change port in `app.py` or stop other services

**Problem:** Tests failing
- **Solution:** Ensure all dependencies are installed correctly

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [example_usage.py](example_usage.py) for code examples
- Explore the web interface at http://localhost:5000
- Try the CLI with your own documents

## Need Help?

- Check the README for detailed documentation
- Review example_usage.py for code samples
- Run tests to verify installation: `pytest test_analyzer.py -v`

## Tips

- Use the web interface for interactive analysis
- Use the CLI for batch processing
- Use the Python API for integration with other tools
- Always review machine-generated analysis with legal expertise
