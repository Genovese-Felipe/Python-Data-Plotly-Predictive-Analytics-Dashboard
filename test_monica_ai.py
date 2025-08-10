#!/usr/bin/env python3
"""
Monica AI System Test Script
============================

Tests the core functionality of the Monica AI Bot System
to ensure all components are working correctly.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Monica_AI_System.core.bot_manager import BotManager
from Monica_AI_System.core.api_integration import APIIntegrationFramework
from Monica_AI_System.core.prompt_system import PromptSystem
from Monica_AI_System.capabilities.knowledge_manager import KnowledgeManager
from Monica_AI_System.capabilities.writing_assistant import WritingAssistant, ContentSpecification

def test_bot_manager():
    """Test bot creation and management."""
    print("🤖 Testing Bot Manager...")
    
    bot_manager = BotManager()
    
    # Create a test bot
    bot_id = bot_manager.create_bot(
        name="Test Assistant",
        role="General Assistant",
        description="Test bot for validation",
        capabilities=["general_assistance", "conversation"],
        knowledge_domains=["general", "technology"],
        communication_style="Professional",
        difficulty_level="Intermediate"
    )
    
    print(f"   ✅ Bot created with ID: {bot_id}")
    
    # Test bot retrieval
    bot = bot_manager.get_bot(bot_id)
    assert bot is not None, "Bot retrieval failed"
    print(f"   ✅ Bot retrieved: {bot.name}")
    
    # Test prompt generation
    prompt = bot_manager.generate_prompt(bot_id, "Test context")
    assert len(prompt) > 0, "Prompt generation failed"
    print(f"   ✅ Prompt generated (length: {len(prompt)})")
    
    # Test analytics
    analytics = bot_manager.get_bot_analytics(bot_id)
    assert analytics is not None, "Analytics failed"
    print(f"   ✅ Analytics retrieved")
    
    print("   🎉 Bot Manager tests passed!\n")

def test_api_integration():
    """Test API integration framework."""
    print("🔌 Testing API Integration Framework...")
    
    api_framework = APIIntegrationFramework()
    
    # Test API status
    status = api_framework.get_api_status()
    assert isinstance(status, dict), "API status failed"
    print(f"   ✅ API status retrieved ({len(status)} APIs)")
    
    # Test supported APIs
    supported = api_framework.get_supported_apis()
    assert len(supported) > 0, "Supported APIs failed"
    print(f"   ✅ Supported APIs: {len(supported)}")
    
    print("   🎉 API Integration tests passed!\n")

def test_prompt_system():
    """Test prompt system functionality."""
    print("📝 Testing Prompt System...")
    
    prompt_system = PromptSystem()
    
    # Test template listing
    templates = prompt_system.list_templates()
    assert len(templates) > 0, "Template listing failed"
    print(f"   ✅ Templates available: {len(templates)}")
    
    # Test prompt generation
    if templates:
        template = templates[0]
        variables = {
            "bot_name": "Test Bot",
            "role": "Assistant",
            "communication_style": "Professional",
            "difficulty_level": "Intermediate",
            "user_query": "Test query"
        }
        
        prompt, execution_id = prompt_system.generate_prompt(
            template.template_id, variables, "test_bot", "test_user"
        )
        
        assert len(prompt) > 0, "Prompt generation failed"
        assert len(execution_id) > 0, "Execution ID failed"
        print(f"   ✅ Prompt generated (execution: {execution_id})")
    
    print("   🎉 Prompt System tests passed!\n")

def test_knowledge_manager():
    """Test knowledge management functionality."""
    print("📚 Testing Knowledge Manager...")
    
    knowledge_manager = KnowledgeManager()
    
    # Test content upload
    test_content = """
    This is a test document for Monica AI system.
    It contains information about artificial intelligence,
    machine learning, and natural language processing.
    """
    
    success, doc_id, message = knowledge_manager.upload_knowledge(
        content=test_content,
        filename="test_document.txt",
        tags=["test", "ai", "machine_learning"]
    )
    
    assert success, f"Knowledge upload failed: {message}"
    print(f"   ✅ Knowledge uploaded: {doc_id}")
    
    # Test search
    results = knowledge_manager.search_knowledge("artificial intelligence", max_results=5)
    print(f"   ✅ Search completed: {len(results)} results")
    
    # Test statistics
    stats = knowledge_manager.get_knowledge_statistics()
    assert stats is not None, "Statistics failed"
    print(f"   ✅ Statistics: {stats.get('total_documents', 0)} documents")
    
    print("   🎉 Knowledge Manager tests passed!\n")

async def test_writing_assistant():
    """Test writing assistant functionality."""
    print("✍️ Testing Writing Assistant...")
    
    writing_assistant = WritingAssistant()
    
    # Test title and outline generation
    title, outline = await writing_assistant.generate_title_and_outline(
        topic="Artificial Intelligence in Business",
        content_type="blog_post",
        target_audience="business professionals",
        research=False
    )
    
    assert len(title) > 0, "Title generation failed"
    assert len(outline) > 0, "Outline generation failed"
    print(f"   ✅ Title: {title}")
    print(f"   ✅ Outline: {len(outline)} sections")
    
    # Test content generation
    specs = ContentSpecification(
        content_type="blog_post",
        length="short",
        tone="professional",
        target_audience="developers",
        purpose="educational",
        format_requirements={},
        research_requirements=False
    )
    
    content = await writing_assistant.generate_content(
        topic="Python Programming",
        specifications=specs
    )
    
    assert content is not None, "Content generation failed"
    assert len(content.content) > 0, "Content is empty"
    print(f"   ✅ Content generated: {content.word_count} words")
    print(f"   ✅ Quality score: {content.quality_score:.2f}")
    
    print("   🎉 Writing Assistant tests passed!\n")

async def main():
    """Run all tests."""
    print("🧪 Monica AI System Test Suite")
    print("=" * 50)
    
    try:
        # Run synchronous tests
        test_bot_manager()
        test_api_integration()
        test_prompt_system()
        test_knowledge_manager()
        
        # Run asynchronous tests
        await test_writing_assistant()
        
        print("🎉 ALL TESTS PASSED!")
        print("\n✨ Monica AI System is fully operational!")
        print("🚀 Ready to enhance your productivity with AI assistance!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())