"""
The main orchestrator for the knowledge extraction pipeline.

This module provides the `KnowledgeExtractionOrchestrator` class, which is
responsible for coordinating the entire workflow of the knowledge extraction
system. It manages the sequence of operations, from file discovery to content
extraction, semantic processing, and final output generation.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import os
import shutil

from tqdm import tqdm
import pandas as pd
import networkx as nx

# Import processors and configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))
from processors.content_extractor import ContentExtractor
from processors.semantic_processor import SemanticProcessor
from config.config import config


class KnowledgeExtractionOrchestrator:
    """
    Orchestrates the entire knowledge extraction and processing pipeline.

    This class coordinates the different stages of the process, including:
    - Discovering files in the knowledge base.
    - Extracting content using the ContentExtractor.
    - Processing semantic features with the SemanticProcessor.
    - Building knowledge structures like embeddings and graphs.
    - Generating the final, structured outputs.
    """

    def __init__(self, knowledge_base_path: Optional[Path] = None):
        """
        Initializes the KnowledgeExtractionOrchestrator.

        Args:
            knowledge_base_path (Optional[Path]): The path to the knowledge base
                directory. If None, it uses the path from the global config.
        """
        self.knowledge_base_path = knowledge_base_path or config.KNOWLEDGE_BASE_DIR
        self.output_dir = config.OUTPUT_DIR
        self.content_extractor = ContentExtractor()
        self.semantic_processor = SemanticProcessor()
        self.extracted_documents: List[Dict[str, Any]] = []
        self.processing_log: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self._setup_output_directories()

    def run_full_extraction(self) -> Dict[str, Any]:
        """
        Runs the complete knowledge extraction pipeline from start to finish.

        This method executes all the steps in the extraction process, from
        discovering files to generating the final summary report.

        Returns:
            A dictionary summarizing the results of the extraction process.
        """
        print("🚀 Starting Knowledge Extraction System...")
        self.start_time = datetime.now()

        try:
            file_catalog = self._discover_files()
            self._extract_all_content(file_catalog)
            self._process_semantics()
            self._build_knowledge_structures()
            self._generate_outputs()
            summary = self._create_summary_report()
            print(f"\n✅ Knowledge extraction completed successfully in {datetime.now() - self.start_time}!")
            return summary
        except Exception as e:
            error_msg = f"❌ Knowledge extraction failed: {e}"
            self._log_message(error_msg, "ERROR")
            return {"status": "failed", "error": str(e)}

    def _discover_files(self) -> List[Dict[str, Any]]:
        """
        Discovers all supported files in the knowledge base directory.

        Returns:
            A list of dictionaries, where each dictionary contains information
            about a discovered file.
        """
        print("\n📂 Discovering files in Knowledge-Base...")
        file_catalog = []
        all_extensions = [ext for ext_list in config.SUPPORTED_FILE_TYPES.values() for ext in ext_list]
        for root, _, files in os.walk(self.knowledge_base_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in all_extensions:
                    file_catalog.append({"path": file_path})
        print(f"Found {len(file_catalog)} files to process.")
        return file_catalog

    def _extract_all_content(self, file_catalog: List[Dict[str, Any]]):
        """
        Extracts content from all discovered files using the ContentExtractor.

        Args:
            file_catalog: A list of file information from the discovery phase.
        """
        print("\n📄 Extracting content from files...")
        for file_info in tqdm(file_catalog, desc="Extracting content"):
            content_data = self.content_extractor.extract_from_file(file_info["path"])
            if content_data.get("extraction_status") == "success":
                self.extracted_documents.append(content_data)

    def _process_semantics(self):
        """Processes semantic features for all extracted documents."""
        print("\n🧠 Processing semantic analysis...")
        for i, doc in enumerate(tqdm(self.extracted_documents, desc="Semantic analysis")):
            self.extracted_documents[i] = self.semantic_processor.process_document_semantics(doc)

    def _build_knowledge_structures(self):
        """Builds the knowledge graph and generates vector embeddings."""
        print("\n🕸️ Building knowledge graph and embeddings...")
        self.semantic_processor.generate_embeddings(self.extracted_documents)
        self.semantic_processor.build_knowledge_graph(self.extracted_documents)

    def _generate_outputs(self):
        """Generates and saves all the final output files."""
        print("\n📊 Generating AI-ready knowledge artifacts...")
        # Save processed documents
        processed_docs_path = self.output_dir / config.OUTPUT_STRUCTURE["processed_content"] / "documents.json"
        self._save_json(self.extracted_documents, processed_docs_path)

        # Save knowledge graph
        kg_path = self.output_dir / config.OUTPUT_STRUCTURE["knowledge_graph"] / "knowledge_graph.json"
        self._save_json(nx.node_link_data(self.semantic_processor.knowledge_graph), kg_path)

    def _create_summary_report(self) -> Dict[str, Any]:
        """
        Creates a final summary report of the extraction process.

        Returns:
            A dictionary containing the summary report.
        """
        print("\n📋 Creating summary report...")
        summary = {
            "processing_info": {"start_time": self.start_time.isoformat() if self.start_time else None, "end_time": datetime.now().isoformat()},
            "extraction_statistics": self.content_extractor.get_extraction_stats(),
            "semantic_statistics": self.semantic_processor.get_semantic_summary(),
        }
        summary_path = self.output_dir / "summary_report.json"
        self._save_json(summary, summary_path)
        return summary

    def _setup_output_directories(self):
        """Creates the necessary output directory structure."""
        for dir_name in config.OUTPUT_STRUCTURE.values():
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)

    def _log_message(self, message: str, level: str = "INFO"):
        """Logs a message to the console and the processing log."""
        log_entry = {"timestamp": datetime.now().isoformat(), "level": level, "message": message}
        self.processing_log.append(log_entry)
        print(f"[{level}] {message}")

    def _save_json(self, data: Any, file_path: Path):
        """Saves data to a JSON file."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)