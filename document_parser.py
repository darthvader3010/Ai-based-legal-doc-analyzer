"""
Document parser module for extracting text from various file formats.
"""

import os
from typing import Optional
import PyPDF2
from docx import Document


class DocumentParser:
    """Parse legal documents from various formats."""
    
    SUPPORTED_FORMATS = ['.pdf', '.docx', '.txt']
    
    def __init__(self):
        pass
    
    def parse(self, file_path: str) -> str:
        """
        Parse a document and extract text content.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats: {', '.join(self.SUPPORTED_FORMATS)}")
        
        try:
            if ext == '.pdf':
                return self._parse_pdf(file_path)
            elif ext == '.docx':
                return self._parse_docx(file_path)
            elif ext == '.txt':
                return self._parse_txt(file_path)
        except Exception as e:
            raise RuntimeError(f"Error parsing document: {str(e)}")
    
    def _parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = []
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        except Exception as e:
            raise RuntimeError(f"Error parsing PDF: {str(e)}")
    
    def _parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            raise RuntimeError(f"Error parsing DOCX: {str(e)}")
    
    def _parse_txt(self, file_path: str) -> str:
        """Extract text from plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise RuntimeError(f"Error parsing TXT: {str(e)}")
