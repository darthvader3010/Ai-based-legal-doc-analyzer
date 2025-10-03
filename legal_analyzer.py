"""
Main legal document analyzer that orchestrates all components.
"""

from typing import Dict, List, Optional
from document_parser import DocumentParser
from text_analyzer import TextAnalyzer
from summarizer import DocumentSummarizer


class LegalDocumentAnalyzer:
    """Main class for analyzing legal documents."""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.analyzer = TextAnalyzer()
        self.summarizer = DocumentSummarizer()
    
    def analyze_document(self, file_path: str) -> Dict:
        """
        Perform complete analysis of a legal document.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing analysis results
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
            RuntimeError: If parsing fails
        """
        try:
            # Parse document
            text = self.parser.parse(file_path)
            
            if not text or len(text.strip()) < 50:
                raise ValueError("Document appears to be empty or too short")
            
            # Extract sections
            clauses = self.analyzer.extract_clauses(text)
            definitions = self.analyzer.extract_definitions(text)
            obligations = self.analyzer.extract_obligations(text)
            
            # Generate summary
            summary = self.summarizer.summarize(text)
            key_points = self.summarizer.generate_key_points(
                text, clauses, definitions, obligations
            )
            
            # Compile results
            results = {
                'success': True,
                'file_path': file_path,
                'text_length': len(text),
                'word_count': len(text.split()),
                'clauses': clauses,
                'definitions': definitions,
                'obligations': obligations,
                'summary': summary,
                'key_points': key_points,
                'full_text': text[:1000]  # First 1000 chars for preview
            }
            
            return results
            
        except (ValueError, FileNotFoundError, RuntimeError) as e:
            # Re-raise expected exceptions
            raise
        except Exception as e:
            # Wrap unexpected exceptions
            raise RuntimeError(f"Unexpected error during analysis: {str(e)}")
    
    def search_document(self, file_path: str, keywords: List[str]) -> Dict:
        """
        Search for keywords in a document.
        
        Args:
            file_path: Path to the document file
            keywords: List of keywords to search for
            
        Returns:
            Dictionary containing search results
        """
        try:
            # Parse document
            text = self.parser.parse(file_path)
            
            # Search keywords
            search_results = self.analyzer.search_keywords(text, keywords)
            
            results = {
                'success': True,
                'file_path': file_path,
                'keywords': keywords,
                'results': search_results,
                'total_matches': sum(len(matches) for matches in search_results.values())
            }
            
            return results
            
        except Exception as e:
            raise RuntimeError(f"Error searching document: {str(e)}")
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return self.parser.SUPPORTED_FORMATS
