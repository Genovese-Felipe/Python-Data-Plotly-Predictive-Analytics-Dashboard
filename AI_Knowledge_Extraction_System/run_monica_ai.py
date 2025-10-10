#!/usr/bin/env python3
"""
Run Monica AI - Enhanced AI Knowledge Processing System

This script provides easy access to the Monica AI interface for comprehensive
knowledge analysis combining local Knowledge-Base with web search capabilities.

Usage:
    python run_monica_ai.py                          # Run with default AI queries
    python run_monica_ai.py --custom                 # Run with custom queries
    python run_monica_ai.py --queries "AI help" "ML" # Run with specific queries
"""

import sys
import argparse
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from monica_ai_interface import MonicaAIInterface

def main():
    """Parses command-line arguments and runs the Monica AI system.

    This function serves as the main entry point for the command-line script.
    It handles argument parsing for different modes of operation, such as
    running with default queries, custom queries, or in test mode.

    Returns:
        An integer status code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="Monica AI - Enhanced AI Knowledge Processing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Run with default AI queries
  %(prog)s --custom                           # Interactive custom query mode
  %(prog)s --queries "Python AI" "Dash ML"   # Run with specific queries
  %(prog)s --test                             # Run basic functionality test
        """
    )
    
    parser.add_argument(
        '--custom', 
        action='store_true',
        help='Interactive mode to enter custom queries'
    )
    
    parser.add_argument(
        '--queries', 
        nargs='+',
        help='Specific queries to process'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run basic functionality test'
    )
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running Monica AI Test Suite...")
        from test_monica_ai import test_monica_ai_basic
        success = test_monica_ai_basic()
        sys.exit(0 if success else 1)
    
    # Initialize Monica AI
    monica_ai = MonicaAIInterface()
    
    custom_queries = None
    
    if args.custom:
        print("\n🤖 Monica AI - Interactive Query Mode")
        print("Enter your queries (one per line, empty line to finish):")
        custom_queries = []
        while True:
            query = input("Query: ").strip()
            if not query:
                break
            custom_queries.append(query)
        
        if not custom_queries:
            print("No queries entered. Using default AI queries.")
            custom_queries = None
    
    elif args.queries:
        custom_queries = args.queries
        print(f"\n🎯 Processing {len(custom_queries)} custom queries...")
        for i, query in enumerate(custom_queries, 1):
            print(f"  {i}. {query}")
    
    # Run comprehensive analysis
    try:
        results = monica_ai.run_comprehensive_analysis(custom_queries)
        
        print(f"\n✅ Monica AI analysis completed successfully!")
        print(f"📄 Results saved to: AI_Knowledge_Extraction_System/outputs/monica_ai_results/")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error running Monica AI: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())