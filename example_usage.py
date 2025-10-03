"""
Example usage of the Legal Document Analyzer.

This script demonstrates how to use the analyzer programmatically.
"""

from legal_analyzer import LegalDocumentAnalyzer


def main():
    """Demonstrate analyzer usage."""
    
    # Initialize the analyzer
    analyzer = LegalDocumentAnalyzer()
    
    print("=" * 60)
    print("Legal Document Analyzer - Example Usage")
    print("=" * 60)
    print()
    
    # Example 1: Get supported formats
    print("Supported formats:")
    formats = analyzer.get_supported_formats()
    print(f"  {', '.join(formats)}")
    print()
    
    # Example 2: Analyze a document
    print("Example 1: Analyzing a document")
    print("-" * 60)
    
    document_path = "path/to/your/document.pdf"  # Replace with actual path
    
    print(f"Note: To analyze a document, use:")
    print(f"  results = analyzer.analyze_document('{document_path}')")
    print()
    print("Results will include:")
    print("  - summary: Concise document summary")
    print("  - clauses: List of extracted clauses")
    print("  - definitions: Key terms and definitions")
    print("  - obligations: Legal obligations and requirements")
    print("  - key_points: Actionable key points")
    print("  - word_count: Total word count")
    print()
    
    # Example 3: Search for keywords
    print("Example 2: Searching for keywords")
    print("-" * 60)
    
    keywords = ["liability", "warranty", "termination", "confidentiality"]
    
    print(f"Note: To search for keywords, use:")
    print(f"  results = analyzer.search_document('{document_path}', {keywords})")
    print()
    print("Results will include:")
    print("  - results: Dictionary mapping keywords to context snippets")
    print("  - total_matches: Total number of matches found")
    print("  - keywords: List of searched keywords")
    print()
    
    # Example 4: Sample code
    print("Example 3: Complete code example")
    print("-" * 60)
    print("""
try:
    # Analyze document
    results = analyzer.analyze_document('contract.pdf')
    
    if results['success']:
        print(f"Document analyzed successfully!")
        print(f"Word count: {results['word_count']}")
        print(f"Clauses found: {len(results['clauses'])}")
        print(f"Summary: {results['summary'][:200]}...")
        
        # Display key points
        print("\\nKey Points:")
        for point in results['key_points']:
            print(f"  • {point}")
    
    # Search for keywords
    search_results = analyzer.search_document(
        'contract.pdf',
        ['indemnification', 'liability']
    )
    
    print(f"\\nFound {search_results['total_matches']} matches")
    for keyword, matches in search_results['results'].items():
        print(f"  {keyword}: {len(matches)} occurrences")
        
except FileNotFoundError:
    print("Error: Document file not found")
except ValueError as e:
    print(f"Error: {e}")
except RuntimeError as e:
    print(f"Error analyzing document: {e}")
    """)
    print()
    
    print("=" * 60)
    print("For web interface usage, run: python app.py")
    print("Then navigate to: http://localhost:5000")
    print("=" * 60)


if __name__ == "__main__":
    main()
