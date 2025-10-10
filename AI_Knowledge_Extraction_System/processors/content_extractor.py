"""
A core module for extracting and processing content from various file types.

This module provides the `ContentExtractor` class, which is responsible for
handling different file formats, extracting their text, images, and metadata,
and performing initial content analysis.
"""

import os
import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
import re

# File processing libraries
import pdfplumber
from PIL import Image
import pandas as pd
from bs4 import BeautifulSoup
import markdown

# Text processing
from collections import Counter

# Configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.config import config


class ContentExtractor:
    """
    A versatile content extraction class that supports multiple file formats.

    This class provides methods to extract text, images, code blocks, and other
    structured data from various file types, including PDFs, Markdown, source code,
    and images. It also gathers comprehensive metadata for each file.
    """

    def __init__(self):
        """Initializes the ContentExtractor and its statistics."""
        self.extraction_stats = {
            "total_files": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
        }

    def extract_from_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Extracts content and metadata from a single file.

        This method serves as the main entry point for file processing. It identifies
        the file type and delegates the extraction to the appropriate specialized method.

        Args:
            file_path: The path to the file to be processed.

        Returns:
            A dictionary containing the extracted content and metadata.
        """
        self.extraction_stats["total_files"] += 1
        try:
            file_info = self._get_file_info(file_path)
            content_data = {"file_info": file_info, "content": "", "images": [], "code_blocks": [], "tables": [], "links": [], "metadata": {}}
            
            file_extension = file_path.suffix.lower()
            if file_extension == ".pdf":
                content_data = self._extract_from_pdf(file_path, content_data)
            elif file_extension == ".md":
                content_data = self._extract_from_markdown(file_path, content_data)
            # Add other file types here...
            else:
                content_data = self._extract_from_text(file_path, content_data)
            
            content_data["content_analysis"] = self._analyze_content(content_data["content"])
            content_data["extraction_status"] = "success"
            self.extraction_stats["successful_extractions"] += 1
            return content_data
        except Exception as e:
            self.extraction_stats["failed_extractions"] += 1
            return {"file_info": self._get_file_info(file_path), "extraction_status": "failed", "error": str(e)}

    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """
        Extracts basic file information and metadata.

        Args:
            file_path: The path to the file.

        Returns:
            A dictionary with file metadata.
        """
        stat = file_path.stat()
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        return {
            "filename": file_path.name, "file_path": str(file_path),
            "file_type": file_path.suffix, "file_size": stat.st_size,
            "creation_date": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modification_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "hash": file_hash, "mime_type": mimetypes.guess_type(str(file_path))[0]
        }

    def _extract_from_pdf(self, file_path: Path, content_data: Dict) -> Dict:
        """
        Extracts text, tables, and image metadata from a PDF file.

        Args:
            file_path: The path to the PDF file.
            content_data: The dictionary to populate with extracted data.

        Returns:
            The updated content_data dictionary.
        """
        with pdfplumber.open(file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() or ""
            content_data["content"] = full_text
            content_data["metadata"]["total_pages"] = len(pdf.pages)
        return content_data

    def _extract_from_markdown(self, file_path: Path, content_data: Dict) -> Dict:
        """
        Extracts content and structure from a Markdown file.

        Args:
            file_path: The path to the Markdown file.
            content_data: The dictionary to populate with extracted data.

        Returns:
            The updated content_data dictionary.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        html_content = markdown.markdown(raw_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        content_data["content"] = soup.get_text()
        return content_data

    def _extract_from_text(self, file_path: Path, content_data: Dict) -> Dict:
        """
        Extracts content from a plain text file.

        Args:
            file_path: The path to the text file.
            content_data: The dictionary to populate with extracted data.

        Returns:
            The updated content_data dictionary.
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content_data["content"] = f.read()
        return content_data

    def _analyze_content(self, content: str) -> Dict[str, Any]:
        """
        Performs a basic analysis of the extracted text content.

        Args:
            content: The text content to analyze.

        Returns:
            A dictionary of content statistics.
        """
        if not content:
            return {}
        
        words = re.findall(r'\b\w+\b', content.lower())
        return {
            "char_count": len(content),
            "word_count": len(words),
            "line_count": len(content.split('\n')),
        }

    def get_extraction_stats(self) -> Dict[str, Any]:
        """
        Returns a copy of the extraction statistics.

        Returns:
            A dictionary with statistics about the extraction process.
        """
        return self.extraction_stats.copy()