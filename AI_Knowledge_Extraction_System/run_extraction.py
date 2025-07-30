"""
Main execution script for the AI Knowledge Extraction System
Run this script to process all Knowledge-Base content and generate AI-ready artifacts
"""

import sys
import os
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from core.orchestrator import KnowledgeExtractionOrchestrator

def main():
    """Main execution function"""
    
    print("=" * 80)
    print("🤖 AI KNOWLEDGE EXTRACTION SYSTEM")
    print("Expert-level content processing for Knowledge-Base materials")
    print("=" * 80)
    
    try:
        # Initialize the orchestrator
        orchestrator = KnowledgeExtractionOrchestrator()
        
        # Run the full extraction pipeline
        summary = orchestrator.run_full_extraction()
        
        if summary.get("status") != "failed":
            print("\n" + "=" * 80)
            print("🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            
            # Print key statistics
            content_stats = summary.get("content_statistics", {})
            print(f"📊 Total documents processed: {content_stats.get('total_documents', 0)}")
            
            file_dist = content_stats.get("file_type_distribution", {})
            if file_dist:
                print("\n📁 File type distribution:")
                for file_type, count in file_dist.items():
                    print(f"  • {file_type}: {count} files")
            
            domain_dist = content_stats.get("domain_distribution", {})
            if domain_dist:
                print("\n🎯 Domain distribution:")
                for domain, count in domain_dist.items():
                    print(f"  • {domain}: {count} documents")
            
            processing_info = summary.get("processing_info", {})
            duration = processing_info.get("processing_duration")
            if duration:
                print(f"\n⏱️ Processing time: {duration}")
            
            print(f"\n📂 All outputs saved in: AI_Knowledge_Extraction_System/outputs/")
            print("\n🔍 Key output files:")
            print("  • documents.json - All processed content")
            print("  • embeddings.json - Vector embeddings for similarity search")
            print("  • knowledge_graph.json - Relationship graph between concepts")
            print("  • training_data.json - AI-ready training data format")
            print("  • documents_analysis.csv - Spreadsheet for analysis")
            print("  • summary_report.json - Complete processing summary")
            
        else:
            print("\\n❌ EXTRACTION FAILED")
            print(f"Error: {summary.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"\\n💥 CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)