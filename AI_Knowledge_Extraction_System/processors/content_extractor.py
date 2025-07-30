"""
Content Processor - Core module for extracting and processing content from various file types
Implements expert-level content extraction with semantic understanding
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
import unicodedata

# Configuration
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config.config import config

class ContentExtractor:
    """Main content extraction class supporting multiple file formats"""
    
    def __init__(self):
        self.processed_files = {}
        self.extraction_stats = {
            "total_files": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "total_content_size": 0
        }
    
    def extract_from_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract content from a single file with comprehensive metadata
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dictionary containing extracted content and metadata
        """
        try:
            file_info = self._get_file_info(file_path)
            content_data = {
                "file_info": file_info,
                "content": "",
                "images": [],
                "code_blocks": [],
                "tables": [],
                "links": [],
                "metadata": {},
                "extraction_status": "pending"
            }
            
            # Determine file type and extract accordingly
            file_extension = file_path.suffix.lower()
            
            if file_extension == ".pdf":
                content_data = self._extract_from_pdf(file_path, content_data)
            elif file_extension == ".md":
                content_data = self._extract_from_markdown(file_path, content_data)
            elif file_extension in [".py", ".js", ".jsx", ".html", ".css", ".xml"]:
                content_data = self._extract_from_code(file_path, content_data)
            elif file_extension in [".png", ".jpg", ".jpeg", ".gif", ".bmp"]:
                content_data = self._extract_from_image(file_path, content_data)
            elif file_extension == ".json":
                content_data = self._extract_from_json(file_path, content_data)
            elif file_extension == ".ipynb":
                content_data = self._extract_from_notebook(file_path, content_data)
            else:
                content_data = self._extract_from_text(file_path, content_data)
            
            # Add content analysis
            content_data["content_analysis"] = self._analyze_content(content_data["content"])
            content_data["extraction_status"] = "success"
            
            self.extraction_stats["successful_extractions"] += 1
            self.extraction_stats["total_content_size"] += len(content_data["content"])
            
            return content_data
            
        except Exception as e:
            self.extraction_stats["failed_extractions"] += 1
            return {
                "file_info": self._get_file_info(file_path),
                "content": "",
                "extraction_status": "failed",
                "error": str(e)
            }
    
    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Extract basic file information and metadata"""
        stat = file_path.stat()
        
        # Calculate file hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        return {
            "filename": file_path.name,
            "file_path": str(file_path),
            "file_type": file_path.suffix.lower(),
            "file_size": stat.st_size,
            "creation_date": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modification_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "hash": file_hash,
            "mime_type": mimetypes.guess_type(str(file_path))[0]
        }
    
    def _extract_from_pdf(self, file_path: Path, content_data: Dict) -> Dict:
        """Extract content from PDF files including text and images"""
        try:
            with pdfplumber.open(file_path) as pdf:
                full_text = ""
                tables = []
                
                for page_num, page in enumerate(pdf.pages):
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        full_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    
                    # Extract tables
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        tables.append({
                            "page": page_num + 1,
                            "data": table,
                            "headers": table[0] if table else []
                        })
                    
                    # Extract images (metadata only for now)
                    if hasattr(page, 'images'):
                        for img in page.images:
                            content_data["images"].append({
                                "page": page_num + 1,
                                "bbox": img.get('bbox', []),
                                "width": img.get('width', 0),
                                "height": img.get('height', 0)
                            })
                
                content_data["content"] = full_text
                content_data["tables"] = tables
                content_data["metadata"]["total_pages"] = len(pdf.pages)
                
        except Exception as e:
            content_data["content"] = f"PDF extraction failed: {str(e)}"
            
        return content_data
    
    def _extract_from_markdown(self, file_path: Path, content_data: Dict) -> Dict:
        """Extract content from Markdown files with structure analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            # Parse markdown
            md = markdown.Markdown(extensions=['meta', 'tables', 'codehilite'])
            html_content = md.convert(raw_content)
            
            # Extract structure using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract headers for structure
            headers = []
            for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                headers.append({
                    "level": int(header.name[1]),
                    "text": header.get_text().strip(),
                    "id": header.get('id', '')
                })
            
            # Extract code blocks
            code_blocks = []
            for code in soup.find_all('code'):
                if code.parent.name == 'pre':
                    code_blocks.append({
                        "language": code.get('class', [''])[0].replace('language-', ''),
                        "content": code.get_text()
                    })
            
            # Extract links
            links = []
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if href:
                    links.append({
                        "text": link.get_text().strip(),
                        "url": href,
                        "type": "external" if href.startswith(('http', 'https')) else "internal"
                    })
            
            content_data["content"] = raw_content
            content_data["code_blocks"] = code_blocks
            content_data["links"] = links
            content_data["metadata"]["headers"] = headers
            content_data["metadata"]["has_frontmatter"] = hasattr(md, 'Meta') and bool(md.Meta)
            
        except Exception as e:
            content_data["content"] = f"Markdown extraction failed: {str(e)}"
            
        return content_data
    
    def _extract_from_code(self, file_path: Path, content_data: Dict) -> Dict:
        """Extract content from code files with syntax analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # Basic code analysis
            lines = code_content.split('\n')
            
            # Extract comments and docstrings
            comments = []
            docstrings = []
            imports = []
            functions = []
            classes = []
            
            in_multiline_comment = False
            comment_buffer = []
            
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                
                # Python-specific parsing
                if file_path.suffix == '.py':
                    if stripped.startswith('#'):
                        comments.append({"line": line_num, "content": stripped[1:].strip()})
                    elif stripped.startswith('"""') or stripped.startswith("'''"):
                        if not in_multiline_comment:
                            in_multiline_comment = True
                            comment_buffer = [stripped]
                        else:
                            comment_buffer.append(stripped)
                            docstrings.append({"lines": f"{line_num - len(comment_buffer) + 1}-{line_num}", 
                                             "content": '\\n'.join(comment_buffer)})
                            in_multiline_comment = False
                            comment_buffer = []
                    elif in_multiline_comment:
                        comment_buffer.append(stripped)
                    elif stripped.startswith('import ') or stripped.startswith('from '):
                        imports.append({"line": line_num, "statement": stripped})
                    elif stripped.startswith('def '):
                        func_match = re.match(r'def\s+(\w+)\s*\(([^)]*)\)', stripped)
                        if func_match:
                            functions.append({
                                "line": line_num,
                                "name": func_match.group(1),
                                "parameters": func_match.group(2).strip()
                            })
                    elif stripped.startswith('class '):
                        class_match = re.match(r'class\s+(\w+).*:', stripped)
                        if class_match:
                            classes.append({
                                "line": line_num,
                                "name": class_match.group(1)
                            })
            
            content_data["content"] = code_content
            content_data["metadata"]["language"] = self._detect_language(file_path)
            content_data["metadata"]["line_count"] = len(lines)
            content_data["metadata"]["comments"] = comments
            content_data["metadata"]["docstrings"] = docstrings
            content_data["metadata"]["imports"] = imports
            content_data["metadata"]["functions"] = functions
            content_data["metadata"]["classes"] = classes
            
        except Exception as e:
            content_data["content"] = f"Code extraction failed: {str(e)}"
            
        return content_data
    
    def _extract_from_image(self, file_path: Path, content_data: Dict) -> Dict:
        """Extract metadata and basic analysis from image files"""
        try:
            with Image.open(file_path) as img:
                content_data["content"] = f"Image file: {file_path.name}"
                content_data["metadata"]["dimensions"] = img.size
                content_data["metadata"]["mode"] = img.mode
                content_data["metadata"]["format"] = img.format
                
                # Basic image analysis
                if img.mode == 'RGB':
                    # Get dominant colors (simplified)
                    img_small = img.resize((50, 50))
                    colors = img_small.getcolors(2500)
                    if colors:
                        dominant_color = max(colors, key=lambda x: x[0])[1]
                        content_data["metadata"]["dominant_color"] = dominant_color
                
        except Exception as e:
            content_data["content"] = f"Image extraction failed: {str(e)}"
            
        return content_data
    
    def _extract_from_json(self, file_path: Path, content_data: Dict) -> Dict:
        """Extract and analyze JSON files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            content_data["content"] = json.dumps(json_data, indent=2)
            content_data["metadata"]["json_structure"] = self._analyze_json_structure(json_data)
            
        except Exception as e:
            content_data["content"] = f"JSON extraction failed: {str(e)}"
            
        return content_data
    
    def _extract_from_notebook(self, file_path: Path, content_data: Dict) -> Dict:
        """Extract content from Jupyter notebooks"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                notebook_data = json.load(f)
            
            # Extract markdown and code cells
            markdown_content = []
            code_content = []
            
            for cell in notebook_data.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    markdown_content.extend(cell.get('source', []))
                elif cell.get('cell_type') == 'code':
                    code_content.extend(cell.get('source', []))
            
            full_content = "MARKDOWN CONTENT:\n" + ''.join(markdown_content)
            full_content += "\n\nCODE CONTENT:\n" + ''.join(code_content)
            
            content_data["content"] = full_content
            content_data["metadata"]["cell_count"] = len(notebook_data.get('cells', []))
            content_data["metadata"]["kernel_spec"] = notebook_data.get('metadata', {}).get('kernelspec', {})
            
        except Exception as e:
            content_data["content"] = f"Notebook extraction failed: {str(e)}"
            
        return content_data
    
    def _extract_from_text(self, file_path: Path, content_data: Dict) -> Dict:
        """Extract content from plain text files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            content_data["content"] = text_content
            
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin1') as f:
                    text_content = f.read()
                content_data["content"] = text_content
                content_data["metadata"]["encoding"] = "latin1"
            except Exception as e:
                content_data["content"] = f"Text extraction failed: {str(e)}"
        
        return content_data
    
    def _analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze extracted content for basic statistics and properties"""
        if not content:
            return {}
        
        analysis = {
            "char_count": len(content),
            "word_count": len(content.split()),
            "line_count": len(content.split('\n')),
            "paragraph_count": len([p for p in content.split('\n\n') if p.strip()]),
            "language_detected": "en",  # Placeholder - would use langdetect in full implementation
            "reading_time_minutes": max(1, len(content.split()) // 200),  # Rough estimate
        }
        
        # Extract potential keywords (simple approach)
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = Counter(words)
        # Filter out common words (basic stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        filtered_words = {word: freq for word, freq in word_freq.items() if word not in stop_words and len(word) > 3}
        analysis["top_keywords"] = dict(sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:20])
        
        return analysis
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.xml': 'xml',
            '.json': 'json',
            '.md': 'markdown',
            '.yml': 'yaml',
            '.yaml': 'yaml'
        }
        return ext_to_lang.get(file_path.suffix.lower(), 'unknown')
    
    def _analyze_json_structure(self, data: Any, max_depth: int = 3, current_depth: int = 0) -> Dict:
        """Analyze JSON structure recursively"""
        if current_depth >= max_depth:
            return {"type": type(data).__name__, "truncated": True}
        
        if isinstance(data, dict):
            return {
                "type": "object",
                "keys": list(data.keys())[:10],  # Limit keys shown
                "key_count": len(data),
                "nested_structure": {k: self._analyze_json_structure(v, max_depth, current_depth + 1) 
                                   for k, v in list(data.items())[:5]}  # Analyze first 5 items
            }
        elif isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "item_types": list(set(type(item).__name__ for item in data[:10])),
                "sample_structure": self._analyze_json_structure(data[0], max_depth, current_depth + 1) if data else None
            }
        else:
            return {"type": type(data).__name__, "sample_value": str(data)[:100]}
    
    def get_extraction_stats(self) -> Dict[str, Any]:
        """Return extraction statistics"""
        return self.extraction_stats.copy()