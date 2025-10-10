#!/usr/bin/env python3
"""
A command-line interface to run the Monica AI knowledge processing system.

This script provides a user-friendly way to interact with the Monica AI system,
offering several modes of operation:
- Running with default, predefined queries.
- Running with custom queries provided as command-line arguments.
- An interactive mode for entering multiple custom queries.
- A test mode to verify basic functionality.

Usage examples:
    - `python run_monica_ai.py`
    - `python run_monica_ai.py --custom`
    - `python run_monica_ai.py --queries "AI in data visualization" "Dash best practices"`
    - `python run_monica_ai.py --test`
"""

import sys
import argparse
from pathlib import Path

# Ensure the parent directory is in the Python path to resolve local imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from monica_ai_interface import MonicaAIInterface

def main():
    """
    The main function to parse command-line arguments and run the Monica AI system.

    This function sets up an argument parser to handle different user inputs,
    initializes the Monica AI interface, and triggers the comprehensive analysis
    based on the selected mode.

    Returns:
        An integer exit code (0 for success, 1 for failure).
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
    
    parser.add_argument('--custom', action='store_true', help='Run in interactive mode to enter custom queries.')
    parser.add_argument('--queries', nargs='+', help='Provide specific queries to process.')
    parser.add_argument('--test', action='store_true', help='Run a basic functionality test.')
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running Monica AI Test Suite...")
        try:
            from test_monica_ai import test_monica_ai_basic
            success = test_monica_ai_basic()
            sys.exit(0 if success else 1)
        except ImportError:
            print("❌ Test file not found. Could not run tests.")
            sys.exit(1)
    
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
            print("No queries entered. Using default queries.")
    
    elif args.queries:
        custom_queries = args.queries
        print(f"\n🎯 Processing {len(custom_queries)} custom queries...")
        for i, query in enumerate(custom_queries, 1):
            print(f"  {i}. {query}")
    
    try:
        monica_ai.run_comprehensive_analysis(custom_queries)
        print(f"\n✅ Monica AI analysis completed successfully!")
        print(f"📄 Results saved to: {monica_ai.output_dir / 'monica_ai_results'}")
        return 0
    except Exception as e:
        print(f"\n❌ An error occurred while running Monica AI: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())