"""
Document summarizer module using NLP techniques.
"""

import re
from typing import List, Dict


class DocumentSummarizer:
    """Generate summaries of legal documents."""
    
    def __init__(self):
        self.max_summary_sentences = 10
    
    def summarize(self, text: str, max_sentences: int = None) -> str:
        """
        Generate a summary of the document.
        
        Args:
            text: Document text
            max_sentences: Maximum number of sentences in summary
            
        Returns:
            Summary text
        """
        if max_sentences is None:
            max_sentences = self.max_summary_sentences
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        if not sentences:
            return "No content to summarize."
        
        # Score sentences based on legal importance
        scored_sentences = self._score_sentences(sentences, text)
        
        # Sort by score and select top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = scored_sentences[:max_sentences]
        
        # Sort by original order
        top_sentences.sort(key=lambda x: x[2])
        
        # Create summary
        summary = ' '.join([sent[0] for sent in top_sentences])
        
        return summary
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        return sentences
    
    def _score_sentences(self, sentences: List[str], full_text: str) -> List[tuple]:
        """
        Score sentences based on importance for legal documents.
        
        Returns:
            List of tuples (sentence, score, original_index)
        """
        scored = []
        
        # Important legal keywords
        important_keywords = [
            'shall', 'must', 'agreement', 'party', 'parties', 'obligation',
            'rights', 'liability', 'warranty', 'indemnify', 'breach',
            'termination', 'jurisdiction', 'dispute', 'clause', 'section',
            'payment', 'compensation', 'damages', 'force majeure', 'confidential'
        ]
        
        for idx, sentence in enumerate(sentences):
            score = 0
            sentence_lower = sentence.lower()
            
            # Score based on important keywords
            for keyword in important_keywords:
                if keyword in sentence_lower:
                    score += 2
            
            # Boost sentences with numbers (likely to be specific terms)
            if re.search(r'\d+', sentence):
                score += 1
            
            # Boost sentences with quoted terms (definitions)
            if '"' in sentence:
                score += 2
            
            # Boost sentences at the beginning (often more important)
            if idx < len(sentences) * 0.2:
                score += 1
            
            # Penalize very long sentences
            if len(sentence) > 500:
                score -= 1
            
            # Position-based scoring
            position_score = 1.0 - (idx / len(sentences)) * 0.3
            score *= position_score
            
            scored.append((sentence, score, idx))
        
        return scored
    
    def generate_key_points(self, text: str, clauses: List[Dict], 
                          definitions: List[Dict], obligations: List[str]) -> List[str]:
        """
        Generate key actionable points from the analysis.
        
        Args:
            text: Full document text
            clauses: Extracted clauses
            definitions: Extracted definitions
            obligations: Extracted obligations
            
        Returns:
            List of key points
        """
        key_points = []
        
        # Add summary of structure
        if clauses:
            key_points.append(f"Document contains {len(clauses)} identifiable clauses/sections")
        
        if definitions:
            key_points.append(f"Found {len(definitions)} key definitions")
            # Add first few important definitions
            for defn in definitions[:3]:
                key_points.append(f"• Defines '{defn['term']}'")
        
        if obligations:
            key_points.append(f"Identified {len(obligations)} obligation statements")
            # Add first few obligations
            for obl in obligations[:3]:
                key_points.append(f"• {obl[:150]}...")
        
        # Analyze for critical legal terms
        critical_terms = ['termination', 'liability', 'warranty', 'indemnification', 
                         'dispute resolution', 'confidentiality', 'payment terms']
        
        found_terms = []
        text_lower = text.lower()
        for term in critical_terms:
            if term in text_lower:
                found_terms.append(term)
        
        if found_terms:
            key_points.append(f"Critical sections present: {', '.join(found_terms)}")
        
        return key_points
