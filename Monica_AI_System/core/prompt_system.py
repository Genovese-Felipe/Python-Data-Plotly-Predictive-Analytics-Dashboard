"""
Monica AI Prompt System
=======================

Advanced prompt engineering and optimization system that provides:
- Structured prompt templates with role-based customization
- Automatic prompt optimization and improvement
- Context-aware prompt generation
- Multi-language prompt support
- Prompt performance analytics and A/B testing
- Dynamic prompt adaptation based on user feedback
"""

import re
import json
import time
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from Monica_AI_System.config.settings import get_config

@dataclass
class PromptTemplate:
    """Structured prompt template definition."""
    template_id: str
    name: str
    description: str
    template_text: str
    variables: List[str]
    category: str
    language: str = "en"
    difficulty_level: str = "intermediate"
    tags: List[str] = None
    created_at: str = ""
    updated_at: str = ""
    usage_count: int = 0
    success_rate: float = 0.0
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

@dataclass
class PromptExecution:
    """Record of prompt execution for analytics."""
    execution_id: str
    template_id: str
    bot_id: str
    user_id: str
    generated_prompt: str
    context: Dict[str, Any]
    response_quality: Optional[float] = None
    execution_time: float = 0.0
    success: bool = True
    user_feedback: Optional[str] = None
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class PromptSystem:
    """
    Advanced prompt engineering and optimization system.
    
    Manages prompt templates, generates context-aware prompts,
    optimizes prompt performance, and provides analytics.
    """
    
    def __init__(self):
        self.config = get_config("bot")
        self.writing_config = get_config("writing")
        self.templates: Dict[str, PromptTemplate] = {}
        self.executions: List[PromptExecution] = []
        self.optimization_rules: Dict[str, Callable] = {}
        
        self._initialize_default_templates()
        self._initialize_optimization_rules()
    
    def _initialize_default_templates(self):
        """Initialize default prompt templates for different use cases."""
        
        # General Assistant Template
        self.add_template(
            name="General Assistant",
            description="Versatile assistant for general inquiries",
            template_text="""You are {bot_name}, a {communication_style} AI assistant specializing in {role}.

Your expertise includes:
{capabilities}

Knowledge domains:
{knowledge_domains}

Communication guidelines:
- Maintain a {communication_style} tone
- Adjust complexity to {difficulty_level} level
- Provide {response_length} responses
- {include_examples_instruction}
- {include_sources_instruction}

Current context: {context}

User query: {user_query}

Please provide a helpful and accurate response.""",
            variables=["bot_name", "communication_style", "role", "capabilities", "knowledge_domains", 
                      "difficulty_level", "response_length", "include_examples_instruction", 
                      "include_sources_instruction", "context", "user_query"],
            category="general"
        )
        
        # Code Development Template
        self.add_template(
            name="Code Developer",
            description="Specialized template for code development assistance",
            template_text="""You are {bot_name}, an expert {programming_language} developer and {role}.

Technical expertise:
{capabilities}

Code quality standards:
- Write clean, readable, and maintainable code
- Follow {programming_language} best practices
- Include appropriate comments and documentation
- Consider performance and security implications
- Provide {difficulty_level}-level explanations

Development context:
- Project type: {project_type}
- Framework/Libraries: {frameworks}
- Requirements: {requirements}

Current task: {user_query}

Please provide code solutions with explanations.""",
            variables=["bot_name", "role", "programming_language", "capabilities", "difficulty_level",
                      "project_type", "frameworks", "requirements", "user_query"],
            category="development"
        )
        
        # Data Analysis Template
        self.add_template(
            name="Data Analyst",
            description="Template for data analysis and insights",
            template_text="""You are {bot_name}, a professional data analyst and {role}.

Analysis capabilities:
{capabilities}

Data context:
- Dataset: {dataset_description}
- Size: {data_size}
- Key variables: {key_variables}
- Analysis objectives: {objectives}

Analytical approach:
- Use {analysis_methods} methods
- Focus on {insight_type} insights
- Present findings at {difficulty_level} level
- Include visualizations if relevant

Query: {user_query}

Please provide comprehensive data analysis and insights.""",
            variables=["bot_name", "role", "capabilities", "dataset_description", "data_size",
                      "key_variables", "objectives", "analysis_methods", "insight_type", 
                      "difficulty_level", "user_query"],
            category="analytics"
        )
        
        # Content Writing Template
        self.add_template(
            name="Content Writer",
            description="Template for content creation and writing assistance",
            template_text="""You are {bot_name}, a skilled {role} with expertise in {writing_specialty}.

Writing capabilities:
{capabilities}

Content specifications:
- Format: {content_format}
- Tone: {tone}
- Length: {content_length}
- Target audience: {target_audience}
- Purpose: {content_purpose}
- Style guidelines: {style_guidelines}

Research context:
{research_context}

Content brief: {user_query}

Please create high-quality content following the specifications.""",
            variables=["bot_name", "role", "writing_specialty", "capabilities", "content_format",
                      "tone", "content_length", "target_audience", "content_purpose", 
                      "style_guidelines", "research_context", "user_query"],
            category="writing"
        )
        
        # Research Assistant Template
        self.add_template(
            name="Research Assistant",
            description="Template for research and information gathering",
            template_text="""You are {bot_name}, a thorough research assistant and {role}.

Research capabilities:
{capabilities}

Research parameters:
- Topic: {research_topic}
- Scope: {research_scope}
- Depth: {difficulty_level}
- Sources: {source_types}
- Methodology: {research_methodology}

Quality standards:
- Verify information from multiple sources
- Cite sources appropriately
- Identify conflicting information
- Provide balanced perspectives
- Organize findings logically

Research request: {user_query}

Please conduct comprehensive research and present findings.""",
            variables=["bot_name", "role", "capabilities", "research_topic", "research_scope",
                      "difficulty_level", "source_types", "research_methodology", "user_query"],
            category="research"
        )
    
    def _initialize_optimization_rules(self):
        """Initialize prompt optimization rules."""
        
        def improve_clarity(prompt: str) -> str:
            """Improve prompt clarity by adding specific instructions."""
            if "please" not in prompt.lower():
                prompt += "\n\nPlease be specific and detailed in your response."
            return prompt
        
        def add_structure(prompt: str) -> str:
            """Add structural elements to prompt."""
            if "format:" not in prompt.lower():
                prompt += "\n\nFormat your response with clear headings and bullet points where appropriate."
            return prompt
        
        def enhance_context(prompt: str) -> str:
            """Enhance context awareness."""
            if "consider" not in prompt.lower():
                prompt += "\n\nConsider the user's experience level and provide appropriate explanations."
            return prompt
        
        self.optimization_rules = {
            "clarity": improve_clarity,
            "structure": add_structure,
            "context": enhance_context
        }
    
    def add_template(
        self,
        name: str,
        description: str,
        template_text: str,
        variables: List[str],
        category: str = "general",
        language: str = "en",
        difficulty_level: str = "intermediate",
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Add a new prompt template.
        
        Args:
            name: Template name
            description: Template description
            template_text: Template with {variable} placeholders
            variables: List of variable names used in template
            category: Template category
            language: Language code
            difficulty_level: Complexity level
            tags: Optional tags for categorization
            
        Returns:
            str: Template ID
        """
        
        template_id = hashlib.md5(f"{name}_{category}_{int(time.time())}".encode()).hexdigest()[:12]
        
        template = PromptTemplate(
            template_id=template_id,
            name=name,
            description=description,
            template_text=template_text,
            variables=variables,
            category=category,
            language=language,
            difficulty_level=difficulty_level,
            tags=tags or []
        )
        
        self.templates[template_id] = template
        return template_id
    
    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """Get template by ID."""
        return self.templates.get(template_id)
    
    def list_templates(self, category: str = None, language: str = None) -> List[PromptTemplate]:
        """List templates with optional filtering."""
        templates = list(self.templates.values())
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        if language:
            templates = [t for t in templates if t.language == language]
        
        return templates
    
    def generate_prompt(
        self,
        template_id: str,
        variables: Dict[str, Any],
        bot_id: str = "",
        user_id: str = "",
        optimize: bool = True
    ) -> Tuple[str, str]:
        """
        Generate a prompt from template with variable substitution.
        
        Args:
            template_id: Template to use
            variables: Dictionary of variable values
            bot_id: Bot ID for analytics
            user_id: User ID for analytics
            optimize: Whether to apply optimization rules
            
        Returns:
            Tuple[str, str]: (generated_prompt, execution_id)
        """
        
        template = self.templates.get(template_id)
        if not template:
            return "", ""
        
        # Generate execution ID
        execution_id = hashlib.md5(f"{template_id}_{bot_id}_{user_id}_{int(time.time())}".encode()).hexdigest()[:16]
        
        # Start with base template
        prompt = template.template_text
        
        # Substitute variables
        for var_name, value in variables.items():
            placeholder = "{" + var_name + "}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        
        # Handle missing variables with defaults
        prompt = self._handle_missing_variables(prompt, template.category)
        
        # Apply optimization if requested
        if optimize:
            prompt = self.optimize_prompt(prompt, template.category)
        
        # Record execution
        execution = PromptExecution(
            execution_id=execution_id,
            template_id=template_id,
            bot_id=bot_id,
            user_id=user_id,
            generated_prompt=prompt,
            context=variables
        )
        self.executions.append(execution)
        
        # Update template usage
        template.usage_count += 1
        template.updated_at = datetime.now().isoformat()
        
        return prompt, execution_id
    
    def _handle_missing_variables(self, prompt: str, category: str) -> str:
        """Handle missing variables in prompt template."""
        
        # Default values for common variables
        defaults = {
            "communication_style": "professional",
            "difficulty_level": "intermediate",
            "response_length": "medium",
            "include_examples_instruction": "Include relevant examples when helpful",
            "include_sources_instruction": "Cite sources when applicable",
            "context": "No additional context provided",
            "capabilities": "General AI assistance capabilities",
            "knowledge_domains": "Broad knowledge across multiple domains"
        }
        
        # Find remaining placeholders
        placeholders = re.findall(r'\{([^}]+)\}', prompt)
        
        for placeholder in placeholders:
            if placeholder in defaults:
                prompt = prompt.replace(f"{{{placeholder}}}", defaults[placeholder])
            else:
                # Remove unfilled placeholders
                prompt = prompt.replace(f"{{{placeholder}}}", "[Not specified]")
        
        return prompt
    
    def optimize_prompt(self, prompt: str, category: str = "general") -> str:
        """
        Apply optimization rules to improve prompt effectiveness.
        
        Args:
            prompt: Original prompt
            category: Prompt category for context-specific optimization
            
        Returns:
            str: Optimized prompt
        """
        
        optimized = prompt
        
        # Apply general optimization rules
        for rule_name, rule_func in self.optimization_rules.items():
            optimized = rule_func(optimized)
        
        # Category-specific optimizations
        if category == "development":
            if "error handling" not in optimized.lower():
                optimized += "\n\nInclude error handling and edge cases in your solution."
        
        elif category == "analytics":
            if "assumptions" not in optimized.lower():
                optimized += "\n\nClearly state any assumptions and limitations in your analysis."
        
        elif category == "writing":
            if "proofread" not in optimized.lower():
                optimized += "\n\nEnsure the content is well-structured and error-free."
        
        return optimized
    
    def auto_optimize_template(self, template_id: str) -> bool:
        """
        Automatically optimize a template based on performance data.
        
        Args:
            template_id: Template to optimize
            
        Returns:
            bool: Success status
        """
        
        template = self.templates.get(template_id)
        if not template:
            return False
        
        # Get executions for this template
        template_executions = [e for e in self.executions if e.template_id == template_id]
        
        if len(template_executions) < 5:  # Need minimum data
            return False
        
        # Analyze common issues
        low_quality_executions = [e for e in template_executions if e.response_quality and e.response_quality < 3.0]
        
        if len(low_quality_executions) > len(template_executions) * 0.3:  # >30% low quality
            # Apply aggressive optimization
            original_text = template.template_text
            optimized_text = self.optimize_prompt(original_text, template.category)
            
            # Add specific improvements based on feedback analysis
            feedback_keywords = []
            for execution in low_quality_executions:
                if execution.user_feedback:
                    feedback_keywords.extend(execution.user_feedback.lower().split())
            
            # Common improvement patterns
            if "unclear" in feedback_keywords or "confusing" in feedback_keywords:
                optimized_text += "\n\nBe explicit and clear in your explanations."
            
            if "too long" in feedback_keywords:
                optimized_text += "\n\nKeep responses concise but comprehensive."
            
            if "missing" in feedback_keywords or "incomplete" in feedback_keywords:
                optimized_text += "\n\nEnsure all aspects of the query are addressed."
            
            # Update template
            template.template_text = optimized_text
            template.updated_at = datetime.now().isoformat()
        
        return True
    
    def record_execution_feedback(
        self,
        execution_id: str,
        response_quality: float,
        user_feedback: str = "",
        execution_time: float = 0.0,
        success: bool = True
    ) -> bool:
        """
        Record feedback for a prompt execution.
        
        Args:
            execution_id: Execution to update
            response_quality: Quality rating (1-5)
            user_feedback: Optional text feedback
            execution_time: Response time in seconds
            success: Whether execution was successful
            
        Returns:
            bool: Success status
        """
        
        for execution in self.executions:
            if execution.execution_id == execution_id:
                execution.response_quality = response_quality
                execution.user_feedback = user_feedback
                execution.execution_time = execution_time
                execution.success = success
                
                # Update template success rate
                template = self.templates.get(execution.template_id)
                if template:
                    template_executions = [e for e in self.executions if e.template_id == execution.template_id]
                    successful_executions = [e for e in template_executions if e.success]
                    template.success_rate = len(successful_executions) / len(template_executions)
                
                return True
        
        return False
    
    def get_template_analytics(self, template_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a template."""
        
        template = self.templates.get(template_id)
        if not template:
            return {}
        
        executions = [e for e in self.executions if e.template_id == template_id]
        
        if not executions:
            return {
                "template_info": {
                    "id": template.template_id,
                    "name": template.name,
                    "category": template.category,
                    "usage_count": template.usage_count
                },
                "performance": {
                    "success_rate": 0.0,
                    "average_quality": 0.0,
                    "average_response_time": 0.0
                }
            }
        
        # Calculate metrics
        quality_scores = [e.response_quality for e in executions if e.response_quality is not None]
        response_times = [e.execution_time for e in executions if e.execution_time > 0]
        
        analytics = {
            "template_info": {
                "id": template.template_id,
                "name": template.name,
                "category": template.category,
                "usage_count": template.usage_count,
                "created_at": template.created_at,
                "updated_at": template.updated_at
            },
            "performance": {
                "total_executions": len(executions),
                "success_rate": template.success_rate,
                "average_quality": sum(quality_scores) / len(quality_scores) if quality_scores else 0.0,
                "average_response_time": sum(response_times) / len(response_times) if response_times else 0.0
            },
            "usage_trends": {
                "last_30_days": len([e for e in executions if (datetime.now() - datetime.fromisoformat(e.timestamp)).days <= 30]),
                "last_7_days": len([e for e in executions if (datetime.now() - datetime.fromisoformat(e.timestamp)).days <= 7])
            }
        }
        
        return analytics
    
    def get_optimization_suggestions(self, template_id: str) -> List[str]:
        """Get optimization suggestions for a template."""
        
        template = self.templates.get(template_id)
        if not template:
            return []
        
        suggestions = []
        analytics = self.get_template_analytics(template_id)
        
        # Performance-based suggestions
        if analytics["performance"]["success_rate"] < 0.7:
            suggestions.append("Consider adding more specific instructions to improve success rate")
        
        if analytics["performance"]["average_quality"] < 3.0:
            suggestions.append("Template may need clearer role definition and better context")
        
        if analytics["performance"]["average_response_time"] > 10.0:
            suggestions.append("Template might be too complex; consider simplifying instructions")
        
        # Content-based suggestions
        template_text = template.template_text.lower()
        
        if len(template.variables) > 15:
            suggestions.append("Consider reducing the number of variables for simpler usage")
        
        if "example" not in template_text:
            suggestions.append("Adding example requests could improve clarity")
        
        if "format" not in template_text:
            suggestions.append("Specify desired response format for consistency")
        
        return suggestions