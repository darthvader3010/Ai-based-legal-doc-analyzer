"""
Text analyzer module for extracting meaningful sections from legal documents.
"""

import re
from typing import List, Dict


class TextAnalyzer:
    """Analyze legal document text to extract sections and key information."""
    
    def __init__(self):
        # Common legal section markers
        self.clause_patterns = [
            r'(?:^|\n)\s*(?:CLAUSE|Article|Section|Paragraph)\s+(\d+[.\d]*)[:\s]',
            r'(?:^|\n)\s*(\d+)\.\s+[A-Z]',
        ]
        
        self.definition_patterns = [
            r'"([^"]+)"\s+(?:means|shall mean|refers to|is defined as)',
            r'(?:^|\n)\s*DEFINITIONS?\s*(?::|$)',
        ]
        
        self.obligation_patterns = [
            r'\b(?:shall|must|will|is required to|is obligated to|agrees to)\b',
            r'\b(?:responsibilities?|obligations?|duties)\b',
        ]
    
    def extract_clauses(self, text: str) -> List[Dict[str, str]]:
        """
        Extract clauses from the document.
        
        Args:
            text: Document text
            
        Returns:
            List of dictionaries containing clause information
        """
        clauses = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            for pattern in self.clause_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    # Get context (current and next few lines)
                    context_lines = lines[i:min(i+5, len(lines))]
                    context = ' '.join(context_lines).strip()
                    
                    clauses.append({
                        'number': match.group(1) if match.lastindex else str(len(clauses) + 1),
                        'text': context[:200] + '...' if len(context) > 200 else context
                    })
                    break
        
        return clauses
    
    def extract_definitions(self, text: str) -> List[Dict[str, str]]:
        """
        Extract definitions from the document.
        
        Args:
            text: Document text
            
        Returns:
            List of dictionaries containing definition information
        """
        definitions = []
        
        # Find quoted terms with definitions
        for match in re.finditer(self.definition_patterns[0], text, re.IGNORECASE):
            term = match.group(1)
            # Get context around the match
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 150)
            context = text[start:end].strip()
            
            definitions.append({
                'term': term,
                'definition': context
            })
        
        return definitions[:20]  # Limit to first 20 definitions
    
    def extract_obligations(self, text: str) -> List[str]:
        """
        Extract obligation sentences from the document.
        
        Args:
            text: Document text
            
        Returns:
            List of sentences containing obligations
        """
        obligations = []
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check if sentence contains obligation keywords
            for pattern in self.obligation_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    if len(sentence) > 20:  # Filter out too short sentences
                        obligations.append(sentence[:200] + '...' if len(sentence) > 200 else sentence)
                    break
        
        return obligations[:15]  # Limit to first 15 obligations
    
    def search_keywords(self, text: str, keywords: List[str]) -> Dict[str, List[str]]:
        """
        Search for keywords in the document and return context.
        
        Args:
            text: Document text
            keywords: List of keywords to search for
            
        Returns:
            Dictionary mapping keywords to list of context snippets
        """
        results = {}
        
        for keyword in keywords:
            matches = []
            # Case-insensitive search
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            
            for match in pattern.finditer(text):
                # Get context around the match
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Highlight the keyword
                context = re.sub(
                    pattern,
                    lambda m: f"**{m.group()}**",
                    context
                )
                
                matches.append(context)
            
            if matches:
                results[keyword] = matches[:10]  # Limit to first 10 matches
        
        return results
