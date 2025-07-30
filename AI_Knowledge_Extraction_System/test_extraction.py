"""
Test script to run extraction on a smaller subset for demonstration
"""

import sys
import os
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from core.orchestrator import KnowledgeExtractionOrchestrator
from config.config import config

def main():
    """Test with limited file types"""
    
    print("🧪 TESTING AI KNOWLEDGE EXTRACTION SYSTEM")
    print("Processing only Markdown and Python files for demonstration...")
    
    # Temporarily modify config to process only specific file types
    original_types = config.SUPPORTED_FILE_TYPES.copy()
    config.SUPPORTED_FILE_TYPES = {
        "documents": [".md"],
        "code": [".py"]
    }
    
    try:
        # Initialize the orchestrator
        orchestrator = KnowledgeExtractionOrchestrator()
        
        # Run the extraction
        summary = orchestrator.run_full_extraction()
        
        if summary.get("status") != "failed":
            print("\n🎉 TEST EXTRACTION COMPLETED!")
            
            # Print key statistics
            content_stats = summary.get("content_statistics", {})
            print(f"📊 Total documents processed: {content_stats.get('total_documents', 0)}")
            
            file_dist = content_stats.get("file_type_distribution", {})
            if file_dist:
                print("\n📁 File type distribution:")
                for file_type, count in file_dist.items():
                    print(f"  • {file_type}: {count} files")
            
            return 0
        else:
            print(f"❌ Test failed: {summary.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"💥 Test error: {str(e)}")
        return 1
    finally:
        # Restore original config
        config.SUPPORTED_FILE_TYPES = original_types

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)