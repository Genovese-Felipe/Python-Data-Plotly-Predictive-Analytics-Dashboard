"""
Test script for Monica AI Interface
Quick test of the enhanced AI Knowledge Extraction System
"""

import sys
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_monica_ai_basic():
    """Test basic Monica AI functionality without full knowledge extraction"""
    print("🧪 Testing Monica AI Interface - Basic Functionality")
    print("="*60)
    
    try:
        from monica_ai_interface import MonicaAIInterface
        
        # Initialize Monica AI
        monica_ai = MonicaAIInterface()
        
        # Test web search processor
        print("\n1️⃣ Testing Web Search Processor...")
        web_results = monica_ai.web_processor.search_duckduckgo("artificial intelligence", 2)
        print(f"   ✅ Web search returned {len(web_results)} results")
        
        # Test multi-query handler with mock data
        print("\n2️⃣ Testing Multi-Query Handler...")
        from core.multi_query_handler import MultiQueryHandler
        
        # Create mock knowledge base data
        mock_knowledge = {
            'documents': [
                {
                    'file_info': {'filename': 'test_ai.md'},
                    'content': 'artificial intelligence machine learning plotly dash visualization',
                    'semantic_analysis': {
                        'keywords': ['ai', 'ml', 'plotly'],
                        'domain_classification': 'data_visualization',
                        'difficulty_level': 'intermediate'
                    }
                }
            ]
        }
        
        query_handler = MultiQueryHandler(mock_knowledge)
        test_queries = ["AI data visualization", "machine learning dashboards"]
        
        query_results = query_handler.process_multiple_queries(test_queries, include_web_search=False)
        print(f"   ✅ Multi-query processing completed for {len(test_queries)} queries")
        print(f"   📊 Confidence: {query_results['comprehensive_synthesis']['confidence_distribution']['average']:.1%}")
        
        # Test AI query generation
        print("\n3️⃣ Testing AI Query Generation...")
        ai_queries = monica_ai._generate_ai_queries()
        print(f"   ✅ Generated {len(ai_queries)} AI-focused queries")
        for i, query in enumerate(ai_queries[:3], 1):
            print(f"      {i}. {query}")
        
        print("\n✅ All basic tests passed!")
        print("Monica AI Interface is ready for comprehensive analysis.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_comprehensive_with_custom_queries():
    """Test comprehensive analysis with custom queries"""
    print("\n" + "="*60)
    print("🚀 Testing Comprehensive Analysis with Custom Queries")
    print("="*60)
    
    try:
        from monica_ai_interface import MonicaAIInterface
        
        monica_ai = MonicaAIInterface()
        
        # Define custom queries focused on the repository
        custom_queries = [
            "Python data visualization best practices",
            "Plotly Dash dashboard development",
            "AI-powered predictive analytics"
        ]
        
        print(f"\n📝 Running comprehensive analysis with {len(custom_queries)} custom queries...")
        
        # Run comprehensive analysis (this will be fast since it uses mock/existing data)
        results = monica_ai.run_comprehensive_analysis(custom_queries)
        
        # Display key results
        monica_data = results['monica_ai_analysis']
        print(f"\n📊 Analysis Results:")
        print(f"   • Session ID: {monica_data['session_info']['session_id']}")
        print(f"   • Processing Time: {monica_data['session_info']['total_processing_time']}")
        print(f"   • Queries Processed: {monica_data['session_info']['queries_processed']}")
        
        print(f"\n✅ Comprehensive analysis completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Comprehensive test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🤖 Monica AI Interface - Test Suite")
    print("Testing enhanced AI Knowledge Extraction System")
    print("="*80)
    
    # Run basic tests
    basic_success = test_monica_ai_basic()
    
    # Run comprehensive test if basic tests pass
    if basic_success:
        comprehensive_success = test_comprehensive_with_custom_queries()
        
        if comprehensive_success:
            print("\n🎉 ALL TESTS PASSED!")
            print("Monica AI Interface is fully functional and ready for use.")
        else:
            print("\n⚠️  Basic tests passed, but comprehensive test failed.")
    else:
        print("\n❌ Basic tests failed. Please check the setup.")
    
    print("\n" + "="*80)