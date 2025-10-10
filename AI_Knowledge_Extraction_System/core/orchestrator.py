"""
Knowledge Extraction Orchestrator
Main coordination system for the expert-level knowledge extraction pipeline
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

# Import our processors
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from processors.content_extractor import ContentExtractor
from processors.semantic_processor import SemanticProcessor
from config.config import config

class KnowledgeExtractionOrchestrator:
    """Orchestrates the entire knowledge extraction and processing pipeline.

    This class serves as the main coordinator for the system, managing the
    workflow from file discovery and content extraction to semantic analysis,
    knowledge graph construction, and final output generation.

    Attributes:
        knowledge_base_path (Path): The file path to the root directory of the
            knowledge base.
        output_dir (Path): The file path to the directory where all processed
            outputs will be saved.
        content_extractor (ContentExtractor): An instance of the content
            extractor.
        semantic_processor (SemanticProcessor): An instance of the semantic
            processor.
        extracted_documents (list): A list to store the dictionaries of
            processed document data.
        processing_log (list): A log of processing steps and events.
        start_time (datetime): The timestamp when the extraction process began.
    """

    def __init__(self, knowledge_base_path: Optional[Path] = None):
        """Initializes the KnowledgeExtractionOrchestrator.

        Args:
            knowledge_base_path: An optional path to the knowledge base. If not
                provided, it defaults to the path specified in the config.
        """
        self.knowledge_base_path = knowledge_base_path or config.KNOWLEDGE_BASE_DIR
        self.output_dir = config.OUTPUT_DIR

        # Initialize processors
        self.content_extractor = ContentExtractor()
        self.semantic_processor = SemanticProcessor()

        # Processing state
        self.extracted_documents = []
        self.processing_log = []
        self.start_time = None

        # Ensure output directories exist
        self._setup_output_directories()

    def run_full_extraction(self) -> Dict[str, Any]:
        """Runs the complete end-to-end knowledge extraction pipeline.

        This is the main public method that executes the entire workflow,
        including file discovery, content extraction, semantic processing,
        and output generation.

        Returns:
            A dictionary containing a summary of the extraction results.
            If the process fails, it returns a dictionary with a 'status'
            of 'failed' and an 'error' message.
        """
        
        print("🚀 Starting Knowledge Extraction System...")
        self.start_time = datetime.now()
        
        try:
            # Step 1: Discover and catalog files
            print("\n📂 Discovering files in Knowledge-Base...")
            file_catalog = self._discover_files()
            print(f"Found {len(file_catalog)} files to process")
            
            # Step 2: Extract content from all files
            print("\n📄 Extracting content from files...")
            self._extract_all_content(file_catalog)
            
            # Step 3: Process semantics for extracted content
            print("\n🧠 Processing semantic analysis...")
            self._process_semantics()
            
            # Step 4: Generate embeddings and knowledge graph
            print("\n🕸️ Building knowledge graph and embeddings...")
            self._build_knowledge_structures()
            
            # Step 5: Perform clustering and topic modeling
            print("\n🔍 Performing clustering and topic modeling...")
            self._perform_advanced_analysis()
            
            # Step 6: Generate AI-ready outputs
            print("\n📊 Generating AI-ready knowledge artifacts...")
            outputs = self._generate_outputs()
            
            # Step 7: Create summary report
            print("\n📋 Creating summary report...")
            summary = self._create_summary_report()
            
            print(f"\n✅ Knowledge extraction completed successfully!")
            print(f"⏱️ Total processing time: {datetime.now() - self.start_time}")
            print(f"📁 Outputs saved to: {self.output_dir}")
            
            return summary
            
        except Exception as e:
            error_msg = f"❌ Knowledge extraction failed: {str(e)}"
            print(error_msg)
            self.processing_log.append({
                "timestamp": datetime.now().isoformat(),
                "level": "ERROR",
                "message": error_msg
            })
            return {"status": "failed", "error": str(e)}
    
    def _discover_files(self) -> List[Dict[str, Any]]:
        """
        Discover all files in the Knowledge-Base directory
        
        Returns:
            List of file information dictionaries
        """
        
        file_catalog = []
        
        # Get all supported file types
        all_extensions = []
        for file_types in config.SUPPORTED_FILE_TYPES.values():
            all_extensions.extend(file_types)
        
        # Walk through directory structure
        for root, dirs, files in os.walk(self.knowledge_base_path):
            for file in files:
                file_path = Path(root) / file
                
                # Check if file type is supported
                if file_path.suffix.lower() in all_extensions:
                    # Check file size
                    try:
                        file_size = file_path.stat().st_size / (1024 * 1024)  # MB
                        if file_size <= config.PROCESSING_CONFIG["max_file_size_mb"]:
                            
                            file_info = {
                                "path": file_path,
                                "relative_path": file_path.relative_to(self.knowledge_base_path),
                                "size_mb": file_size,
                                "extension": file_path.suffix.lower(),
                                "category": self._categorize_file(file_path.suffix.lower())
                            }
                            file_catalog.append(file_info)
                        else:
                            self._log_message(f"Skipping large file: {file_path} ({file_size:.1f}MB)")
                    except OSError as e:
                        self._log_message(f"Error accessing file: {file_path} - {e}")
        
        return file_catalog
    
    def _extract_all_content(self, file_catalog: List[Dict[str, Any]]) -> None:
        """
        Extract content from all discovered files
        
        Args:
            file_catalog: List of file information from discovery
        """
        
        self.extracted_documents = []
        
        for file_info in tqdm(file_catalog, desc="Extracting content"):
            try:
                # Extract content using ContentExtractor
                content_data = self.content_extractor.extract_from_file(file_info["path"])
                
                # Add catalog info
                content_data["catalog_info"] = file_info
                
                # Only keep successfully extracted content
                if content_data.get("extraction_status") == "success":
                    self.extracted_documents.append(content_data)
                    self._log_message(f"Successfully extracted: {file_info['relative_path']}")
                else:
                    self._log_message(f"Failed to extract: {file_info['relative_path']} - {content_data.get('error', 'Unknown error')}")
                    
            except Exception as e:
                self._log_message(f"Error processing {file_info['path']}: {str(e)}")
        
        self._log_message(f"Content extraction completed. {len(self.extracted_documents)} documents processed successfully.")
    
    def _process_semantics(self) -> None:
        """Process semantic analysis for all extracted documents"""
        
        for i, doc in enumerate(tqdm(self.extracted_documents, desc="Semantic analysis")):
            try:
                # Process with semantic processor
                enhanced_doc = self.semantic_processor.process_document_semantics(doc)
                self.extracted_documents[i] = enhanced_doc
                
            except Exception as e:
                self._log_message(f"Semantic processing failed for {doc['file_info']['filename']}: {str(e)}")
    
    def _build_knowledge_structures(self) -> None:
        """Build knowledge graph and generate embeddings"""
        
        try:
            # Generate embeddings
            self._log_message("Generating document embeddings...")
            embeddings = self.semantic_processor.generate_embeddings(self.extracted_documents)
            self._log_message(f"Generated embeddings for {len(embeddings)} documents")
            
            # Build knowledge graph
            self._log_message("Building knowledge graph...")
            knowledge_graph = self.semantic_processor.build_knowledge_graph(self.extracted_documents)
            self._log_message(f"Knowledge graph built with {knowledge_graph.number_of_nodes()} nodes and {knowledge_graph.number_of_edges()} edges")
            
        except Exception as e:
            self._log_message(f"Error building knowledge structures: {str(e)}")
    
    def _perform_advanced_analysis(self) -> None:
        """Perform clustering and topic modeling"""
        
        try:
            # Clustering
            self._log_message("Performing document clustering...")
            clustering_results = self.semantic_processor.perform_clustering(self.extracted_documents)
            if clustering_results:
                self._log_message(f"Created {clustering_results.get('n_clusters', 0)} clusters")
            
            # Topic modeling
            self._log_message("Extracting topics...")
            topic_results = self.semantic_processor.extract_topics(self.extracted_documents)
            if topic_results:
                self._log_message(f"Extracted {topic_results.get('n_topics', 0)} topics")
                
        except Exception as e:
            self._log_message(f"Error in advanced analysis: {str(e)}")
    
    def _generate_outputs(self) -> Dict[str, str]:
        """
        Generate all output files and AI-ready artifacts
        
        Returns:
            Dictionary of generated output file paths
        """
        
        outputs = {}
        
        try:
            # 1. Save processed documents
            processed_docs_path = self.output_dir / config.OUTPUT_STRUCTURE["processed_content"] / "documents.json"
            self._save_json(self.extracted_documents, processed_docs_path)
            outputs["processed_documents"] = str(processed_docs_path)
            
            # 2. Save embeddings
            if self.semantic_processor.document_embeddings:
                embeddings_path = self.output_dir / config.OUTPUT_STRUCTURE["embeddings"] / "embeddings.json"
                # Convert numpy arrays to lists for JSON serialization
                serializable_embeddings = {
                    doc_id: embedding.tolist() 
                    for doc_id, embedding in self.semantic_processor.document_embeddings.items()
                }
                self._save_json(serializable_embeddings, embeddings_path)
                outputs["embeddings"] = str(embeddings_path)
            
            # 3. Save knowledge graph
            if self.semantic_processor.knowledge_graph.number_of_nodes() > 0:
                kg_path = self.output_dir / config.OUTPUT_STRUCTURE["knowledge_graph"] / "knowledge_graph.json"
                kg_data = self._serialize_knowledge_graph()
                self._save_json(kg_data, kg_path)
                outputs["knowledge_graph"] = str(kg_path)
            
            # 4. Generate metadata catalog
            metadata_path = self.output_dir / config.OUTPUT_STRUCTURE["metadata"] / "catalog.json"
            metadata_catalog = self._create_metadata_catalog()
            self._save_json(metadata_catalog, metadata_path)
            outputs["metadata_catalog"] = str(metadata_path)
            
            # 5. Create search index
            index_path = self.output_dir / config.OUTPUT_STRUCTURE["indexes"] / "search_index.json"
            search_index = self._create_search_index()
            self._save_json(search_index, index_path)
            outputs["search_index"] = str(index_path)
            
            # 6. Generate content summaries
            summaries_path = self.output_dir / config.OUTPUT_STRUCTURE["summaries"] / "summaries.json"
            summaries = self._create_content_summaries()
            self._save_json(summaries, summaries_path)
            outputs["summaries"] = str(summaries_path)
            
            # 7. Create AI training data
            ai_data_path = self.output_dir / config.OUTPUT_STRUCTURE["ai_ready"] / "training_data.json"
            ai_training_data = self._create_ai_training_data()
            self._save_json(ai_training_data, ai_data_path)
            outputs["ai_training_data"] = str(ai_data_path)
            
            # 8. Generate CSV exports for easy analysis
            csv_path = self.output_dir / "exports" / "documents_analysis.csv"
            self._create_csv_export(csv_path)
            outputs["csv_export"] = str(csv_path)
            
        except Exception as e:
            self._log_message(f"Error generating outputs: {str(e)}")
        
        return outputs
    
    def _create_summary_report(self) -> Dict[str, Any]:
        """Create a comprehensive summary report"""
        
        end_time = datetime.now()
        processing_time = end_time - self.start_time if self.start_time else None
        
        # Content statistics
        content_stats = {
            "total_documents": len(self.extracted_documents),
            "file_type_distribution": self._get_file_type_distribution(),
            "content_size_stats": self._get_content_size_stats(),
            "domain_distribution": self._get_domain_distribution()
        }
        
        # Processing statistics
        extraction_stats = self.content_extractor.get_extraction_stats()
        semantic_stats = self.semantic_processor.get_semantic_summary()
        
        summary = {
            "processing_info": {
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": end_time.isoformat(),
                "processing_duration": str(processing_time) if processing_time else None,
                "system_version": "1.0.0"
            },
            "content_statistics": content_stats,
            "extraction_statistics": extraction_stats,
            "semantic_statistics": semantic_stats,
            "output_locations": config.OUTPUT_STRUCTURE,
            "processing_log": self.processing_log[-50:]  # Last 50 log entries
        }
        
        # Save summary report
        summary_path = self.output_dir / "summary_report.json"
        self._save_json(summary, summary_path)
        
        return summary
    
    def _setup_output_directories(self) -> None:
        """Create output directory structure"""
        
        base_dirs = [
            self.output_dir,
            self.output_dir / config.OUTPUT_STRUCTURE["processed_content"],
            self.output_dir / config.OUTPUT_STRUCTURE["embeddings"],
            self.output_dir / config.OUTPUT_STRUCTURE["knowledge_graph"],
            self.output_dir / config.OUTPUT_STRUCTURE["metadata"],
            self.output_dir / config.OUTPUT_STRUCTURE["indexes"],
            self.output_dir / config.OUTPUT_STRUCTURE["summaries"],
            self.output_dir / config.OUTPUT_STRUCTURE["ai_ready"],
            self.output_dir / "exports"
        ]
        
        for dir_path in base_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _categorize_file(self, extension: str) -> str:
        """Categorize file based on extension"""
        
        for category, extensions in config.SUPPORTED_FILE_TYPES.items():
            if extension in extensions:
                return category
        return "unknown"
    
    def _log_message(self, message: str, level: str = "INFO") -> None:
        """Add message to processing log"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.processing_log.append(log_entry)
        print(f"[{level}] {message}")
    
    def _save_json(self, data: Any, file_path: Path) -> None:
        """Save data as JSON file"""
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def _serialize_knowledge_graph(self) -> Dict[str, Any]:
        """Serialize knowledge graph to JSON-compatible format"""
        
        kg = self.semantic_processor.knowledge_graph
        
        return {
            "nodes": [
                {
                    "id": node_id,
                    "attributes": dict(attrs)
                }
                for node_id, attrs in kg.nodes(data=True)
            ],
            "edges": [
                {
                    "source": source,
                    "target": target,
                    "attributes": dict(attrs)
                }
                for source, target, attrs in kg.edges(data=True)
            ],
            "statistics": {
                "node_count": kg.number_of_nodes(),
                "edge_count": kg.number_of_edges(),
                "density": float(nx.density(kg)) if kg.number_of_nodes() > 0 else 0.0
            }
        }
    
    def _create_metadata_catalog(self) -> Dict[str, Any]:
        """Create comprehensive metadata catalog"""
        
        catalog = {
            "documents": {},
            "statistics": {
                "total_documents": len(self.extracted_documents),
                "creation_timestamp": datetime.now().isoformat()
            }
        }
        
        for doc in self.extracted_documents:
            doc_id = doc["file_info"]["hash"]
            catalog["documents"][doc_id] = {
                "file_info": doc["file_info"],
                "content_analysis": doc.get("content_analysis", {}),
                "semantic_analysis": doc.get("semantic_analysis", {}),
                "catalog_info": doc.get("catalog_info", {})
            }
        
        return catalog
    
    def _create_search_index(self) -> Dict[str, Any]:
        """Create search index for fast content retrieval"""
        
        index = {
            "documents": {},
            "keywords": {},
            "topics": {},
            "creation_timestamp": datetime.now().isoformat()
        }
        
        for doc in self.extracted_documents:
            doc_id = doc["file_info"]["hash"]
            filename = doc["file_info"]["filename"]
            
            # Document index entry
            index["documents"][doc_id] = {
                "filename": filename,
                "file_path": doc["file_info"]["file_path"],
                "domain": doc.get("semantic_analysis", {}).get("domain_classification", ""),
                "content_type": doc.get("semantic_analysis", {}).get("content_type", ""),
                "keywords": doc.get("semantic_analysis", {}).get("keywords", [])[:10],
                "char_count": doc.get("content_analysis", {}).get("char_count", 0)
            }
            
            # Keyword index
            for keyword in doc.get("semantic_analysis", {}).get("keywords", []):
                if keyword not in index["keywords"]:
                    index["keywords"][keyword] = []
                index["keywords"][keyword].append({
                    "doc_id": doc_id,
                    "filename": filename
                })
        
        return index
    
    def _create_content_summaries(self) -> Dict[str, Any]:
        """Create content summaries for quick reference"""
        
        summaries = {
            "document_summaries": {},
            "cluster_summaries": self.semantic_processor.semantic_clusters.get("summaries", {}),
            "topic_summaries": self.semantic_processor.topic_model.get("topics", {}) if self.semantic_processor.topic_model else {},
            "creation_timestamp": datetime.now().isoformat()
        }
        
        for doc in self.extracted_documents:
            doc_id = doc["file_info"]["hash"]
            content = doc.get("content", "")
            
            # Create simple summary (first 500 characters)
            summary_text = content[:500] + "..." if len(content) > 500 else content
            
            summaries["document_summaries"][doc_id] = {
                "filename": doc["file_info"]["filename"],
                "summary": summary_text,
                "word_count": doc.get("content_analysis", {}).get("word_count", 0),
                "reading_time": doc.get("content_analysis", {}).get("reading_time_minutes", 0),
                "domain": doc.get("semantic_analysis", {}).get("domain_classification", ""),
                "difficulty": doc.get("semantic_analysis", {}).get("difficulty_level", ""),
                "key_topics": doc.get("semantic_analysis", {}).get("topics", [])
            }
        
        return summaries
    
    def _create_ai_training_data(self) -> Dict[str, Any]:
        """Create AI-ready training data format"""
        
        training_data = {
            "documents": [],
            "metadata": {
                "total_documents": len(self.extracted_documents),
                "creation_timestamp": datetime.now().isoformat(),
                "format_version": "1.0",
                "description": "AI-ready knowledge base for Plotly/Dash development"
            }
        }
        
        for doc in self.extracted_documents:
            semantic_info = doc.get("semantic_analysis", {})
            content_info = doc.get("content_analysis", {})
            
            ai_doc = {
                "id": doc["file_info"]["hash"],
                "text": doc.get("processed_content", doc.get("content", "")),
                "metadata": {
                    "filename": doc["file_info"]["filename"],
                    "file_type": doc["file_info"]["file_type"],
                    "domain": semantic_info.get("domain_classification", ""),
                    "content_type": semantic_info.get("content_type", ""),
                    "difficulty_level": semantic_info.get("difficulty_level", ""),
                    "keywords": semantic_info.get("keywords", [])[:10],
                    "topics": semantic_info.get("topics", []),
                    "word_count": content_info.get("word_count", 0),
                    "complexity_score": semantic_info.get("complexity_score", 0)
                },
                "tags": semantic_info.get("semantic_tags", [])
            }
            
            training_data["documents"].append(ai_doc)
        
        return training_data
    
    def _create_csv_export(self, file_path: Path) -> None:
        """Create CSV export for analysis"""
        
        rows = []
        for doc in self.extracted_documents:
            semantic_info = doc.get("semantic_analysis", {})
            content_info = doc.get("content_analysis", {})
            file_info = doc["file_info"]
            
            row = {
                "filename": file_info["filename"],
                "file_type": file_info["file_type"],
                "file_size": file_info["file_size"],
                "domain": semantic_info.get("domain_classification", ""),
                "content_type": semantic_info.get("content_type", ""),
                "difficulty_level": semantic_info.get("difficulty_level", ""),
                "word_count": content_info.get("word_count", 0),
                "char_count": content_info.get("char_count", 0),
                "complexity_score": semantic_info.get("complexity_score", 0),
                "keywords": "; ".join(semantic_info.get("keywords", [])[:5]),
                "topics": "; ".join(semantic_info.get("topics", []))
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False)
    
    def _get_file_type_distribution(self) -> Dict[str, int]:
        """Get distribution of file types"""
        
        distribution = {}
        for doc in self.extracted_documents:
            file_type = doc["file_info"]["file_type"]
            distribution[file_type] = distribution.get(file_type, 0) + 1
        
        return distribution
    
    def _get_content_size_stats(self) -> Dict[str, float]:
        """Get content size statistics"""
        
        word_counts = [doc.get("content_analysis", {}).get("word_count", 0) for doc in self.extracted_documents]
        
        if not word_counts:
            return {}
        
        import numpy as np
        return {
            "mean_word_count": float(np.mean(word_counts)),
            "median_word_count": float(np.median(word_counts)),
            "total_words": int(np.sum(word_counts)),
            "max_word_count": int(np.max(word_counts)),
            "min_word_count": int(np.min(word_counts))
        }
    
    def _get_domain_distribution(self) -> Dict[str, int]:
        """Get distribution of content domains"""
        
        distribution = {}
        for doc in self.extracted_documents:
            domain = doc.get("semantic_analysis", {}).get("domain_classification", "unknown")
            distribution[domain] = distribution.get(domain, 0) + 1
        
        return distribution