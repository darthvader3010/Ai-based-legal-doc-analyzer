"""
Unit tests for the legal document analyzer.
"""

import os
import pytest
import tempfile
from document_parser import DocumentParser
from text_analyzer import TextAnalyzer
from summarizer import DocumentSummarizer
from legal_analyzer import LegalDocumentAnalyzer


# Sample legal text for testing
SAMPLE_LEGAL_TEXT = """
CONFIDENTIALITY AGREEMENT

This Agreement is entered into between Party A and Party B.

DEFINITIONS

"Confidential Information" means any information disclosed by one party to the other party.
"Disclosing Party" refers to the party providing information.

CLAUSE 1: OBLIGATIONS

The Receiving Party shall maintain confidentiality of all Confidential Information.
The Receiving Party must not disclose any information to third parties.

CLAUSE 2: TERM

This Agreement shall remain in effect for a period of two years.

CLAUSE 3: LIABILITY

Each party agrees to indemnify the other party against any claims arising from breach.
The parties shall resolve any disputes through arbitration in accordance with applicable law.
"""


class TestDocumentParser:
    """Tests for DocumentParser class."""
    
    def test_supported_formats(self):
        """Test that supported formats are correctly defined."""
        parser = DocumentParser()
        assert '.pdf' in parser.SUPPORTED_FORMATS
        assert '.docx' in parser.SUPPORTED_FORMATS
        assert '.txt' in parser.SUPPORTED_FORMATS
    
    def test_parse_txt_file(self):
        """Test parsing a plain text file."""
        parser = DocumentParser()
        
        # Create temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(SAMPLE_LEGAL_TEXT)
            temp_path = f.name
        
        try:
            text = parser.parse(temp_path)
            assert len(text) > 0
            assert "CONFIDENTIALITY AGREEMENT" in text
            assert "CLAUSE 1" in text
        finally:
            os.unlink(temp_path)
    
    def test_parse_nonexistent_file(self):
        """Test that parsing nonexistent file raises FileNotFoundError."""
        parser = DocumentParser()
        
        with pytest.raises(FileNotFoundError):
            parser.parse('/nonexistent/file.txt')
    
    def test_parse_unsupported_format(self):
        """Test that unsupported format raises ValueError."""
        parser = DocumentParser()
        
        # Create temporary file with unsupported extension
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write("test")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported file format"):
                parser.parse(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_parse_empty_file(self):
        """Test parsing an empty file."""
        parser = DocumentParser()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            temp_path = f.name
        
        try:
            text = parser.parse(temp_path)
            assert text == ""
        finally:
            os.unlink(temp_path)


class TestTextAnalyzer:
    """Tests for TextAnalyzer class."""
    
    def test_extract_clauses(self):
        """Test clause extraction."""
        analyzer = TextAnalyzer()
        clauses = analyzer.extract_clauses(SAMPLE_LEGAL_TEXT)
        
        assert len(clauses) > 0
        assert any('CLAUSE 1' in str(clause) for clause in clauses)
    
    def test_extract_definitions(self):
        """Test definition extraction."""
        analyzer = TextAnalyzer()
        definitions = analyzer.extract_definitions(SAMPLE_LEGAL_TEXT)
        
        assert len(definitions) > 0
        # Check if key definitions are found
        terms = [d['term'] for d in definitions]
        assert 'Confidential Information' in terms or 'Disclosing Party' in terms
    
    def test_extract_obligations(self):
        """Test obligation extraction."""
        analyzer = TextAnalyzer()
        obligations = analyzer.extract_obligations(SAMPLE_LEGAL_TEXT)
        
        assert len(obligations) > 0
        # Check if obligations with "shall" or "must" are found
        assert any('shall' in obl.lower() or 'must' in obl.lower() for obl in obligations)
    
    def test_search_keywords_found(self):
        """Test keyword search with matches."""
        analyzer = TextAnalyzer()
        results = analyzer.search_keywords(SAMPLE_LEGAL_TEXT, ['confidentiality', 'party'])
        
        assert 'confidentiality' in results or 'Confidentiality' in str(results)
        assert len(results) > 0
    
    def test_search_keywords_not_found(self):
        """Test keyword search with no matches."""
        analyzer = TextAnalyzer()
        results = analyzer.search_keywords(SAMPLE_LEGAL_TEXT, ['nonexistent'])
        
        assert 'nonexistent' not in results or len(results.get('nonexistent', [])) == 0
    
    def test_search_multiple_keywords(self):
        """Test searching for multiple keywords."""
        analyzer = TextAnalyzer()
        keywords = ['Agreement', 'liability', 'arbitration']
        results = analyzer.search_keywords(SAMPLE_LEGAL_TEXT, keywords)
        
        # At least some keywords should be found
        assert len(results) > 0


class TestDocumentSummarizer:
    """Tests for DocumentSummarizer class."""
    
    def test_summarize_basic(self):
        """Test basic summarization."""
        summarizer = DocumentSummarizer()
        summary = summarizer.summarize(SAMPLE_LEGAL_TEXT)
        
        assert len(summary) > 0
        assert len(summary) < len(SAMPLE_LEGAL_TEXT)
    
    def test_summarize_empty_text(self):
        """Test summarizing empty text."""
        summarizer = DocumentSummarizer()
        summary = summarizer.summarize("")
        
        assert "No content to summarize" in summary
    
    def test_summarize_with_max_sentences(self):
        """Test summarization with sentence limit."""
        summarizer = DocumentSummarizer()
        summary = summarizer.summarize(SAMPLE_LEGAL_TEXT, max_sentences=3)
        
        # Summary should exist and be shorter
        assert len(summary) > 0
    
    def test_generate_key_points(self):
        """Test key points generation."""
        summarizer = DocumentSummarizer()
        analyzer = TextAnalyzer()
        
        clauses = analyzer.extract_clauses(SAMPLE_LEGAL_TEXT)
        definitions = analyzer.extract_definitions(SAMPLE_LEGAL_TEXT)
        obligations = analyzer.extract_obligations(SAMPLE_LEGAL_TEXT)
        
        key_points = summarizer.generate_key_points(
            SAMPLE_LEGAL_TEXT, clauses, definitions, obligations
        )
        
        assert len(key_points) > 0
        assert isinstance(key_points, list)


class TestLegalDocumentAnalyzer:
    """Tests for LegalDocumentAnalyzer class."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = LegalDocumentAnalyzer()
        
        assert analyzer.parser is not None
        assert analyzer.analyzer is not None
        assert analyzer.summarizer is not None
    
    def test_analyze_document_success(self):
        """Test successful document analysis."""
        analyzer = LegalDocumentAnalyzer()
        
        # Create temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(SAMPLE_LEGAL_TEXT)
            temp_path = f.name
        
        try:
            results = analyzer.analyze_document(temp_path)
            
            assert results['success'] is True
            assert 'clauses' in results
            assert 'definitions' in results
            assert 'obligations' in results
            assert 'summary' in results
            assert 'key_points' in results
            assert results['word_count'] > 0
        finally:
            os.unlink(temp_path)
    
    def test_analyze_document_file_not_found(self):
        """Test analysis with nonexistent file."""
        analyzer = LegalDocumentAnalyzer()
        
        with pytest.raises(FileNotFoundError):
            analyzer.analyze_document('/nonexistent/file.txt')
    
    def test_analyze_document_unsupported_format(self):
        """Test analysis with unsupported format."""
        analyzer = LegalDocumentAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write(SAMPLE_LEGAL_TEXT)
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError):
                analyzer.analyze_document(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_analyze_document_empty_file(self):
        """Test analysis with empty file."""
        analyzer = LegalDocumentAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Short")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="empty or too short"):
                analyzer.analyze_document(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_search_document_success(self):
        """Test successful keyword search."""
        analyzer = LegalDocumentAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(SAMPLE_LEGAL_TEXT)
            temp_path = f.name
        
        try:
            results = analyzer.search_document(temp_path, ['confidentiality', 'agreement'])
            
            assert results['success'] is True
            assert 'results' in results
            assert 'total_matches' in results
            assert results['total_matches'] >= 0
        finally:
            os.unlink(temp_path)
    
    def test_get_supported_formats(self):
        """Test getting supported formats."""
        analyzer = LegalDocumentAnalyzer()
        formats = analyzer.get_supported_formats()
        
        assert isinstance(formats, list)
        assert len(formats) > 0
        assert '.txt' in formats


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
