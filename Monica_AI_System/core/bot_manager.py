"""
Monica AI Bot Manager
====================

Core bot creation and management system that handles:
- Bot creation with structured prompts and roles
- Bot lifecycle management (create, update, delete, activate)
- Bot personalization and preference management
- Bot performance monitoring and analytics
- Multi-user bot management with permissions
"""

import json
import uuid
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from Monica_AI_System.config.settings import get_config

@dataclass
class BotProfile:
    """Data class representing a Monica AI Bot profile."""
    bot_id: str
    name: str
    role: str
    description: str
    capabilities: List[str]
    knowledge_domains: List[str]
    communication_style: str
    difficulty_level: str
    personalization_settings: Dict[str, Any]
    api_integrations: List[str]
    created_at: str
    updated_at: str
    owner_id: str
    is_active: bool = True
    usage_stats: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.usage_stats is None:
            self.usage_stats = {
                "total_interactions": 0,
                "successful_responses": 0,
                "average_response_time": 0.0,
                "user_satisfaction": 0.0,
                "last_used": None
            }

class BotManager:
    """
    Central bot management system for Monica AI.
    
    Handles all aspects of bot lifecycle including creation, configuration,
    personalization, and performance monitoring.
    """
    
    def __init__(self):
        self.config = get_config("bot")
        self.monica_config = get_config("monica")
        self.bots: Dict[str, BotProfile] = {}
        self.user_bots: Dict[str, List[str]] = {}  # user_id -> [bot_ids]
        
    def create_bot(
        self,
        name: str,
        role: str,
        description: str,
        capabilities: List[str],
        knowledge_domains: List[str],
        communication_style: str = "Professional",
        difficulty_level: str = "Intermediate",
        owner_id: str = "default_user",
        personalization_settings: Optional[Dict[str, Any]] = None,
        api_integrations: Optional[List[str]] = None
    ) -> str:
        """
        Create a new Monica AI bot with specified configuration.
        
        Args:
            name: Bot name/identifier
            role: Bot's primary role (from available_roles)
            description: Detailed description of bot's purpose
            capabilities: List of specific capabilities
            knowledge_domains: Areas of expertise
            communication_style: How the bot communicates
            difficulty_level: Complexity level of responses
            owner_id: User ID who owns this bot
            personalization_settings: Custom user preferences
            api_integrations: List of APIs this bot can use
            
        Returns:
            str: Unique bot ID
        """
        
        # Validate role
        if role not in self.config["available_roles"]:
            raise ValueError(f"Invalid role. Must be one of: {self.config['available_roles']}")
        
        # Validate communication style
        if communication_style not in self.config["communication_styles"]:
            raise ValueError(f"Invalid communication style. Must be one of: {self.config['communication_styles']}")
        
        # Validate difficulty level
        if difficulty_level not in self.config["difficulty_levels"]:
            raise ValueError(f"Invalid difficulty level. Must be one of: {self.config['difficulty_levels']}")
        
        # Check user bot limit
        user_bot_count = len(self.user_bots.get(owner_id, []))
        if user_bot_count >= self.monica_config["max_bots_per_user"]:
            raise ValueError(f"User has reached maximum bot limit: {self.monica_config['max_bots_per_user']}")
        
        # Generate unique bot ID
        bot_id = str(uuid.uuid4())
        
        # Set defaults
        if personalization_settings is None:
            personalization_settings = {
                "response_length_preference": "medium",
                "include_examples": True,
                "include_sources": True,
                "preferred_format": "markdown"
            }
        
        if api_integrations is None:
            api_integrations = ["web_search", "knowledge_base"]
        
        # Create bot profile
        current_time = datetime.datetime.now().isoformat()
        bot_profile = BotProfile(
            bot_id=bot_id,
            name=name,
            role=role,
            description=description,
            capabilities=capabilities,
            knowledge_domains=knowledge_domains,
            communication_style=communication_style,
            difficulty_level=difficulty_level,
            personalization_settings=personalization_settings,
            api_integrations=api_integrations,
            created_at=current_time,
            updated_at=current_time,
            owner_id=owner_id
        )
        
        # Store bot
        self.bots[bot_id] = bot_profile
        
        # Update user bot list
        if owner_id not in self.user_bots:
            self.user_bots[owner_id] = []
        self.user_bots[owner_id].append(bot_id)
        
        return bot_id
    
    def get_bot(self, bot_id: str) -> Optional[BotProfile]:
        """Get bot profile by ID."""
        return self.bots.get(bot_id)
    
    def update_bot(
        self,
        bot_id: str,
        updates: Dict[str, Any],
        owner_id: str = None
    ) -> bool:
        """
        Update bot configuration.
        
        Args:
            bot_id: Bot to update
            updates: Dictionary of fields to update
            owner_id: User ID (for permission check)
            
        Returns:
            bool: Success status
        """
        
        bot = self.bots.get(bot_id)
        if not bot:
            return False
        
        # Check ownership if owner_id provided
        if owner_id and bot.owner_id != owner_id:
            return False
        
        # Update allowed fields
        allowed_fields = {
            'name', 'description', 'capabilities', 'knowledge_domains',
            'communication_style', 'difficulty_level', 'personalization_settings',
            'api_integrations', 'is_active'
        }
        
        for field, value in updates.items():
            if field in allowed_fields and hasattr(bot, field):
                setattr(bot, field, value)
        
        # Update timestamp
        bot.updated_at = datetime.datetime.now().isoformat()
        
        return True
    
    def delete_bot(self, bot_id: str, owner_id: str = None) -> bool:
        """
        Delete a bot.
        
        Args:
            bot_id: Bot to delete
            owner_id: User ID (for permission check)
            
        Returns:
            bool: Success status
        """
        
        bot = self.bots.get(bot_id)
        if not bot:
            return False
        
        # Check ownership if owner_id provided
        if owner_id and bot.owner_id != owner_id:
            return False
        
        # Remove from user's bot list
        if bot.owner_id in self.user_bots:
            if bot_id in self.user_bots[bot.owner_id]:
                self.user_bots[bot.owner_id].remove(bot_id)
        
        # Delete bot
        del self.bots[bot_id]
        
        return True
    
    def list_user_bots(self, owner_id: str) -> List[BotProfile]:
        """Get all bots owned by a user."""
        bot_ids = self.user_bots.get(owner_id, [])
        return [self.bots[bot_id] for bot_id in bot_ids if bot_id in self.bots]
    
    def get_active_bots(self, owner_id: str = None) -> List[BotProfile]:
        """Get all active bots, optionally filtered by owner."""
        if owner_id:
            return [bot for bot in self.list_user_bots(owner_id) if bot.is_active]
        return [bot for bot in self.bots.values() if bot.is_active]
    
    def generate_prompt(self, bot_id: str, context: str = "") -> str:
        """
        Generate a structured prompt for the bot based on its configuration.
        
        Args:
            bot_id: Bot ID
            context: Additional context for the prompt
            
        Returns:
            str: Generated prompt
        """
        
        bot = self.bots.get(bot_id)
        if not bot:
            return ""
        
        # Build capabilities string
        capabilities_str = "\n".join([f"- {cap}" for cap in bot.capabilities])
        
        # Build knowledge domains string
        knowledge_str = "\n".join([f"- {domain}" for domain in bot.knowledge_domains])
        
        # Generate prompt from template
        prompt = self.config["default_prompt_template"].format(
            bot_name=bot.name,
            role=bot.role,
            capabilities=capabilities_str,
            knowledge_domains=knowledge_str,
            communication_style=bot.communication_style,
            difficulty_level=bot.difficulty_level
        )
        
        # Add context if provided
        if context:
            prompt += f"\n\nAdditional context for this interaction:\n{context}"
        
        return prompt
    
    def update_usage_stats(
        self,
        bot_id: str,
        response_time: float,
        success: bool,
        user_rating: Optional[float] = None
    ) -> bool:
        """
        Update bot usage statistics.
        
        Args:
            bot_id: Bot ID
            response_time: Response time in seconds
            success: Whether the response was successful
            user_rating: Optional user satisfaction rating (0-5)
            
        Returns:
            bool: Success status
        """
        
        bot = self.bots.get(bot_id)
        if not bot:
            return False
        
        stats = bot.usage_stats
        
        # Update counters
        stats["total_interactions"] += 1
        if success:
            stats["successful_responses"] += 1
        
        # Update average response time
        current_avg = stats["average_response_time"]
        total = stats["total_interactions"]
        stats["average_response_time"] = ((current_avg * (total - 1)) + response_time) / total
        
        # Update user satisfaction if provided
        if user_rating is not None:
            current_satisfaction = stats["user_satisfaction"]
            if current_satisfaction == 0:
                stats["user_satisfaction"] = user_rating
            else:
                # Simple moving average for satisfaction
                stats["user_satisfaction"] = (current_satisfaction + user_rating) / 2
        
        # Update last used timestamp
        stats["last_used"] = datetime.datetime.now().isoformat()
        
        return True
    
    def get_bot_analytics(self, bot_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a bot."""
        bot = self.bots.get(bot_id)
        if not bot:
            return {}
        
        stats = bot.usage_stats
        
        # Calculate success rate
        success_rate = 0.0
        if stats["total_interactions"] > 0:
            success_rate = stats["successful_responses"] / stats["total_interactions"]
        
        return {
            "bot_info": {
                "id": bot.bot_id,
                "name": bot.name,
                "role": bot.role,
                "created_at": bot.created_at,
                "is_active": bot.is_active
            },
            "usage_statistics": stats,
            "performance_metrics": {
                "success_rate": success_rate,
                "efficiency_score": min(1.0, 10.0 / max(stats["average_response_time"], 0.1)),
                "user_satisfaction_score": stats["user_satisfaction"]
            },
            "configuration": {
                "capabilities_count": len(bot.capabilities),
                "knowledge_domains_count": len(bot.knowledge_domains),
                "api_integrations_count": len(bot.api_integrations),
                "communication_style": bot.communication_style,
                "difficulty_level": bot.difficulty_level
            }
        }
    
    def export_bot_config(self, bot_id: str) -> Optional[Dict[str, Any]]:
        """Export bot configuration for backup or sharing."""
        bot = self.bots.get(bot_id)
        if not bot:
            return None
        
        return asdict(bot)
    
    def import_bot_config(self, config: Dict[str, Any], owner_id: str) -> Optional[str]:
        """Import bot configuration from exported data."""
        try:
            # Generate new bot ID
            new_bot_id = str(uuid.uuid4())
            
            # Create bot profile from config
            bot_profile = BotProfile(**config)
            bot_profile.bot_id = new_bot_id
            bot_profile.owner_id = owner_id
            bot_profile.created_at = datetime.datetime.now().isoformat()
            bot_profile.updated_at = datetime.datetime.now().isoformat()
            
            # Store bot
            self.bots[new_bot_id] = bot_profile
            
            # Update user bot list
            if owner_id not in self.user_bots:
                self.user_bots[owner_id] = []
            self.user_bots[owner_id].append(new_bot_id)
            
            return new_bot_id
            
        except Exception:
            return None