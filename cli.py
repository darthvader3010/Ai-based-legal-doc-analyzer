#!/usr/bin/env python
"""
Command-line interface for the Legal Document Analyzer.
"""

import argparse
import sys
import json
from legal_analyzer import LegalDocumentAnalyzer


def print_analysis_results(results):
    """Print analysis results in a formatted way."""
    print("\n" + "=" * 70)
    print("LEGAL DOCUMENT ANALYSIS RESULTS")
    print("=" * 70)
    
    print(f"\n📄 Document: {results['file_path']}")
    print(f"📊 Word Count: {results['word_count']:,}")
    print(f"📏 Text Length: {results['text_length']:,} characters")
    
    # Summary
    print("\n" + "-" * 70)
    print("📋 SUMMARY")
    print("-" * 70)
    print(results['summary'])
    
    # Key Points
    if results['key_points']:
        print("\n" + "-" * 70)
        print("🎯 KEY POINTS")
        print("-" * 70)
        for point in results['key_points']:
            print(f"  • {point}")
    
    # Clauses
    if results['clauses']:
        print("\n" + "-" * 70)
        print(f"📑 CLAUSES ({len(results['clauses'])})")
        print("-" * 70)
        for clause in results['clauses'][:5]:  # Show first 5
            print(f"  Clause {clause['number']}: {clause['text'][:100]}...")
        if len(results['clauses']) > 5:
            print(f"  ... and {len(results['clauses']) - 5} more")
    
    # Definitions
    if results['definitions']:
        print("\n" + "-" * 70)
        print(f"📖 DEFINITIONS ({len(results['definitions'])})")
        print("-" * 70)
        for defn in results['definitions'][:5]:  # Show first 5
            print(f"  \"{defn['term']}\": {defn['definition'][:80]}...")
        if len(results['definitions']) > 5:
            print(f"  ... and {len(results['definitions']) - 5} more")
    
    # Obligations
    if results['obligations']:
        print("\n" + "-" * 70)
        print(f"⚠️  OBLIGATIONS ({len(results['obligations'])})")
        print("-" * 70)
        for obl in results['obligations'][:5]:  # Show first 5
            print(f"  • {obl[:100]}...")
        if len(results['obligations']) > 5:
            print(f"  ... and {len(results['obligations']) - 5} more")
    
    print("\n" + "=" * 70 + "\n")


def print_search_results(results):
    """Print search results in a formatted way."""
    print("\n" + "=" * 70)
    print("KEYWORD SEARCH RESULTS")
    print("=" * 70)
    
    print(f"\n📄 Document: {results['file_path']}")
    print(f"🔍 Keywords: {', '.join(results['keywords'])}")
    print(f"📊 Total Matches: {results['total_matches']}")
    
    if results['total_matches'] == 0:
        print("\nNo matches found.")
    else:
        for keyword, matches in results['results'].items():
            print("\n" + "-" * 70)
            print(f"Keyword: \"{keyword}\" ({len(matches)} matches)")
            print("-" * 70)
            for i, match in enumerate(matches[:3], 1):  # Show first 3 per keyword
                print(f"\nMatch {i}:")
                print(f"  {match}")
            if len(matches) > 3:
                print(f"\n  ... and {len(matches) - 3} more matches")
    
    print("\n" + "=" * 70 + "\n")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Analyze legal documents from the command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a document
  python cli.py analyze contract.pdf
  
  # Analyze and save to JSON
  python cli.py analyze contract.pdf --json output.json
  
  # Search for keywords
  python cli.py search contract.pdf --keywords "liability,warranty,termination"
  
  # Get supported formats
  python cli.py formats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a legal document')
    analyze_parser.add_argument('file', help='Path to the document file')
    analyze_parser.add_argument('--json', dest='json_output', 
                               help='Save results to JSON file')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for keywords in a document')
    search_parser.add_argument('file', help='Path to the document file')
    search_parser.add_argument('--keywords', required=True,
                              help='Comma-separated list of keywords to search')
    search_parser.add_argument('--json', dest='json_output',
                              help='Save results to JSON file')
    
    # Formats command
    formats_parser = subparsers.add_parser('formats', help='List supported file formats')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = LegalDocumentAnalyzer()
    
    try:
        if args.command == 'formats':
            print("\nSupported file formats:")
            for fmt in analyzer.get_supported_formats():
                print(f"  • {fmt}")
            print()
        
        elif args.command == 'analyze':
            print(f"\nAnalyzing document: {args.file}")
            print("This may take a moment...\n")
            
            results = analyzer.analyze_document(args.file)
            
            if args.json_output:
                with open(args.json_output, 'w') as f:
                    json.dump(results, f, indent=2)
                print(f"Results saved to: {args.json_output}")
            else:
                print_analysis_results(results)
        
        elif args.command == 'search':
            keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
            
            if not keywords:
                print("Error: No valid keywords provided")
                sys.exit(1)
            
            print(f"\nSearching document: {args.file}")
            print(f"Keywords: {', '.join(keywords)}\n")
            
            results = analyzer.search_document(args.file, keywords)
            
            if args.json_output:
                with open(args.json_output, 'w') as f:
                    json.dump(results, f, indent=2)
                print(f"Results saved to: {args.json_output}")
            else:
                print_search_results(results)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)


if __name__ == '__main__':
    main()
