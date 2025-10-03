# AI-Based Legal Document Analyzer

An intelligent legal document analyzer that uses AI and NLP techniques to parse, analyze, and summarize legal documents. This tool helps legal professionals quickly understand key aspects of legal documents including clauses, definitions, obligations, and more.

## Features

- **Multi-Format Support**: Parse PDF, DOCX, and TXT documents
- **Section Extraction**: Automatically identify clauses, definitions, and obligations
- **AI-Powered Summarization**: Generate concise summaries while maintaining legal terminology
- **Keyword Search**: Search for specific terms and view context
- **User-Friendly Web Interface**: Easy-to-use web application for document upload and analysis
- **Robust Error Handling**: Comprehensive error handling for unsupported formats and parsing errors

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/darthvader3010/Ai-based-legal-doc-analyzer.git
cd Ai-based-legal-doc-analyzer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Use the web interface to:
   - Upload legal documents (PDF, DOCX, or TXT)
   - View analysis results including summary, clauses, definitions, and obligations
   - Search for keywords within documents

### Using the API Programmatically

```python
from legal_analyzer import LegalDocumentAnalyzer

# Initialize analyzer
analyzer = LegalDocumentAnalyzer()

# Analyze a document
results = analyzer.analyze_document('path/to/document.pdf')

# Access results
print(f"Summary: {results['summary']}")
print(f"Clauses found: {len(results['clauses'])}")
print(f"Definitions found: {len(results['definitions'])}")
print(f"Obligations found: {len(results['obligations'])}")

# Search for keywords
search_results = analyzer.search_document('path/to/document.pdf', ['liability', 'warranty'])
print(f"Total matches: {search_results['total_matches']}")
```

## Project Structure

```
Ai-based-legal-doc-analyzer/
├── app.py                  # Flask web application
├── legal_analyzer.py       # Main analyzer orchestrator
├── document_parser.py      # Document parsing module
├── text_analyzer.py        # Text analysis and section extraction
├── summarizer.py           # Document summarization
├── test_analyzer.py        # Unit tests
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web interface
└── README.md              # This file
```

## API Endpoints

### POST /upload
Analyze a legal document.

**Request:**
- `file`: Document file (PDF, DOCX, or TXT)

**Response:**
```json
{
  "success": true,
  "clauses": [...],
  "definitions": [...],
  "obligations": [...],
  "summary": "...",
  "key_points": [...],
  "word_count": 1234
}
```

### POST /search
Search for keywords in a document.

**Request:**
- `file`: Document file (PDF, DOCX, or TXT)
- `keywords`: Comma-separated keywords

**Response:**
```json
{
  "success": true,
  "results": {
    "keyword1": ["context1", "context2"],
    "keyword2": ["context3"]
  },
  "total_matches": 3
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "supported_formats": [".pdf", ".docx", ".txt"]
}
```

## Testing

Run the unit tests:

```bash
pytest test_analyzer.py -v
```

Run tests with coverage:

```bash
pytest test_analyzer.py --cov=. --cov-report=html
```

## Features in Detail

### Document Parsing
- **PDF**: Extracts text from PDF files using PyPDF2
- **DOCX**: Parses Word documents using python-docx
- **TXT**: Reads plain text files with UTF-8 encoding

### Text Analysis
- **Clause Detection**: Identifies numbered clauses, articles, and sections
- **Definition Extraction**: Finds defined terms in quotes and definition sections
- **Obligation Identification**: Detects sentences with legal obligations (shall, must, etc.)

### Summarization
- **Importance Scoring**: Ranks sentences based on legal keywords and structure
- **Key Points**: Generates actionable points from the document
- **Term Preservation**: Maintains legal terminology in summaries

### Error Handling
- File not found errors
- Unsupported format detection
- Empty document handling
- Parsing error recovery
- File size limits (16MB max)

## Technologies Used

- **Flask**: Web application framework
- **PyPDF2**: PDF parsing
- **python-docx**: DOCX parsing
- **pytest**: Unit testing
- **HTML/CSS/JavaScript**: Frontend interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Future Enhancements

- Integration with advanced NLP models (e.g., BERT, GPT)
- Support for additional document formats
- Multi-language support
- Document comparison features
- Export analysis results to various formats
- Advanced legal term recognition
- Clause recommendation system