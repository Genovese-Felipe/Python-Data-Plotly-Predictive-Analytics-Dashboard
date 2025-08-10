"""
Monica AI System Configuration
=============================

Central configuration for the Monica AI Bot System including:
- Bot management settings
- API integration configurations  
- Platform-specific settings
- Security and authentication parameters
- Performance and optimization settings
"""

import os
from typing import Dict, List, Any

# Core System Configuration
MONICA_CONFIG = {
    "system_name": "Monica AI Assistant",
    "version": "1.0.0",
    "max_bots_per_user": 10,
    "default_bot_timeout": 30,  # seconds
    "enable_advanced_features": True,
    "enable_multi_platform": True,
    "enable_knowledge_management": True
}

# Bot Creation Configuration
BOT_CONFIG = {
    "default_prompt_template": """
    You are {bot_name}, a specialized AI assistant with the following role: {role}.
    
    Your capabilities include:
    {capabilities}
    
    Your knowledge base covers:
    {knowledge_domains}
    
    Communication style: {communication_style}
    Difficulty level: {difficulty_level}
    
    Always provide helpful, accurate, and contextually relevant responses.
    """,
    
    "available_roles": [
        "General Assistant",
        "Code Developer", 
        "Data Analyst",
        "Content Writer",
        "Research Assistant",
        "Project Manager",
        "Business Consultant",
        "Educational Tutor"
    ],
    
    "communication_styles": [
        "Professional",
        "Friendly",
        "Technical", 
        "Creative",
        "Analytical",
        "Instructional"
    ],
    
    "difficulty_levels": [
        "Beginner",
        "Intermediate", 
        "Advanced",
        "Expert"
    ]
}

# API Integration Configuration
API_CONFIG = {
    "supported_apis": [
        # Communication & Email
        "gmail_api", "outlook_api", "slack_api", "discord_api", "telegram_api",
        
        # Content & Media
        "youtube_api", "twitter_api", "facebook_api", "instagram_api", "linkedin_api",
        "spotify_api", "podcast_api", "news_api",
        
        # Development & Code
        "github_api", "gitlab_api", "stackoverflow_api", "npm_api", "pypi_api",
        "docker_api", "aws_api", "azure_api", "gcp_api",
        
        # Data & Analytics
        "google_analytics", "firebase_api", "mongodb_api", "postgresql_api",
        
        # Search & Knowledge
        "google_search", "bing_search", "wikipedia_api", "wolfram_alpha",
        "arxiv_api", "pubmed_api",
        
        # Productivity
        "notion_api", "trello_api", "asana_api", "jira_api", "zapier_api"
    ],
    
    "api_rate_limits": {
        "default_requests_per_minute": 60,
        "premium_requests_per_minute": 300,
        "burst_limit": 10
    },
    
    "api_timeout": 30,
    "max_retries": 3,
    "enable_caching": True,
    "cache_duration": 3600  # 1 hour
}

# Writing & Communication Configuration
WRITING_CONFIG = {
    "auto_title_generation": True,
    "web_research_enabled": True,
    "max_research_sources": 10,
    "content_formats": [
        "blog_post", "email", "report", "summary", "documentation",
        "social_media", "presentation", "tutorial", "analysis"
    ],
    
    "tone_options": [
        "professional", "casual", "formal", "friendly", "technical",
        "persuasive", "informative", "creative", "analytical"
    ],
    
    "length_options": {
        "short": {"min": 50, "max": 200},
        "medium": {"min": 200, "max": 800}, 
        "long": {"min": 800, "max": 2000},
        "extended": {"min": 2000, "max": 5000}
    }
}

# Search & Analysis Configuration  
SEARCH_CONFIG = {
    "enable_multi_keyword_analysis": True,
    "max_keywords_per_query": 20,
    "enable_result_summarization": True,
    "max_sources_per_summary": 15,
    "enable_related_questions": True,
    "max_related_questions": 10,
    
    "search_engines": [
        "google", "bing", "duckduckgo", "semantic_scholar", "arxiv"
    ],
    
    "content_types": [
        "web_pages", "academic_papers", "news_articles", 
        "documentation", "code_repositories", "videos"
    ]
}

# Platform Integration Configuration
PLATFORM_CONFIG = {
    "gmail": {
        "enable_auto_analysis": True,
        "enable_task_detection": True,
        "enable_quick_responses": True,
        "response_templates": True
    },
    
    "outlook": {
        "enable_auto_analysis": True,
        "enable_task_detection": True,
        "enable_calendar_integration": True
    },
    
    "youtube": {
        "enable_video_summaries": True,
        "enable_timestamp_extraction": True,
        "enable_realtime_qa": True,
        "max_video_length": 7200  # 2 hours
    },
    
    "social_media": {
        "enable_content_generation": True,
        "enable_sentiment_analysis": True,
        "enable_engagement_optimization": True,
        "supported_platforms": ["twitter", "linkedin", "facebook", "instagram"]
    },
    
    "web_navigation": {
        "enable_contextual_assistance": True,
        "enable_page_analysis": True,
        "enable_form_filling": True
    }
}

# Knowledge Management Configuration
KNOWLEDGE_CONFIG = {
    "enable_external_upload": True,
    "supported_file_types": [
        ".pdf", ".docx", ".txt", ".md", ".html", ".json", ".csv",
        ".py", ".js", ".java", ".cpp", ".sql", ".yaml", ".xml"
    ],
    
    "max_file_size_mb": 100,
    "enable_semantic_enrichment": True,
    "enable_auto_categorization": True,
    "enable_relationship_mapping": True,
    
    "vector_embedding": {
        "model": "sentence-transformers",
        "dimension": 384,
        "similarity_threshold": 0.7
    }
}

# Security Configuration
SECURITY_CONFIG = {
    "enable_user_authentication": True,
    "session_timeout": 3600,  # 1 hour
    "max_failed_attempts": 5,
    "enable_rate_limiting": True,
    "enable_content_filtering": True,
    
    "api_keys": {
        "encrypt_storage": True,
        "rotation_interval": 2592000,  # 30 days
        "require_secure_transmission": True
    }
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "enable_caching": True,
    "cache_size_mb": 500,
    "enable_background_processing": True,
    "max_concurrent_requests": 50,
    "enable_load_balancing": True,
    
    "database": {
        "connection_pool_size": 20,
        "query_timeout": 30,
        "enable_query_optimization": True
    }
}

# Development Configuration
DEVELOPMENT_CONFIG = {
    "enable_code_analysis": True,
    "supported_languages": [
        "python", "javascript", "typescript", "java", "cpp", "csharp",
        "go", "rust", "php", "ruby", "sql", "html", "css", "shell"
    ],
    
    "code_quality_checks": True,
    "enable_documentation_generation": True,
    "enable_test_suggestions": True,
    "enable_refactoring_assistance": True
}

# Export all configurations
def get_config(config_name: str = None) -> Dict[str, Any]:
    """Get configuration by name or all configurations."""
    configs = {
        "monica": MONICA_CONFIG,
        "bot": BOT_CONFIG,
        "api": API_CONFIG,
        "writing": WRITING_CONFIG,
        "search": SEARCH_CONFIG,
        "platform": PLATFORM_CONFIG,
        "knowledge": KNOWLEDGE_CONFIG,
        "security": SECURITY_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "development": DEVELOPMENT_CONFIG
    }
    
    if config_name:
        return configs.get(config_name, {})
    return configs

def update_config(config_name: str, updates: Dict[str, Any]) -> bool:
    """Update configuration with new values."""
    try:
        config = get_config(config_name)
        if config:
            config.update(updates)
            return True
        return False
    except Exception:
        return False