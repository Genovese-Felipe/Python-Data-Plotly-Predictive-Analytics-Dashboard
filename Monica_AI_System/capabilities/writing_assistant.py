"""
Monica AI Writing and Communication Capabilities
===============================================

Advanced writing assistance and communication features including:
- Automatic title and outline generation
- Extensive web research integration
- Content creation with detailed specifications
- Quick email response generation with context analysis
- Automatic prompt optimization
- Multi-format content generation (blogs, reports, documentation)
"""

import re
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from Monica_AI_System.core.api_integration import APIIntegrationFramework
from Monica_AI_System.config.settings import get_config

@dataclass
class ContentSpecification:
    """Specifications for content generation."""
    content_type: str  # "blog_post", "email", "report", etc.
    length: str  # "short", "medium", "long", "extended"
    tone: str  # "professional", "casual", "formal", etc.
    target_audience: str
    purpose: str
    format_requirements: Dict[str, Any]
    research_requirements: bool = True
    include_citations: bool = True

@dataclass
class ResearchResult:
    """Research findings from web sources."""
    query: str
    sources: List[Dict[str, Any]]
    key_findings: List[str]
    citations: List[str]
    confidence_score: float
    research_timestamp: str

@dataclass
class GeneratedContent:
    """Generated content with metadata."""
    content_id: str
    title: str
    content: str
    outline: List[str]
    word_count: int
    specifications: ContentSpecification
    research_used: Optional[ResearchResult]
    quality_score: float
    generation_timestamp: str
    revisions: List[str] = None
    
    def __post_init__(self):
        if self.revisions is None:
            self.revisions = []

class WritingAssistant:
    """
    Advanced writing and communication assistant.
    
    Provides intelligent content generation, research integration,
    and communication optimization across multiple formats and contexts.
    """
    
    def __init__(self):
        self.config = get_config("writing")
        self.api_framework = APIIntegrationFramework()
        self.generated_content: Dict[str, GeneratedContent] = {}
        self.research_cache: Dict[str, ResearchResult] = {}
        
        # Initialize writing templates and patterns
        self._initialize_templates()
        self._initialize_optimization_patterns()
    
    def _initialize_templates(self):
        """Initialize content templates for different formats."""
        
        self.templates = {
            "blog_post": {
                "structure": ["introduction", "main_points", "examples", "conclusion"],
                "intro_patterns": [
                    "In today's {context}, {topic} has become increasingly important because {reason}.",
                    "Have you ever wondered about {topic}? This comprehensive guide will {promise}.",
                    "The landscape of {domain} is rapidly evolving, and {topic} represents a significant {impact}."
                ],
                "conclusion_patterns": [
                    "In conclusion, {topic} offers {benefits} for {audience}. The key is to {action}.",
                    "As we've explored, {topic} is essential for {outcome}. Start implementing these {strategies} today.",
                    "The future of {domain} depends on how well we understand and apply {concepts}."
                ]
            },
            
            "email": {
                "structure": ["greeting", "purpose", "main_content", "call_to_action", "closing"],
                "greeting_patterns": {
                    "formal": "Dear {recipient},",
                    "professional": "Hello {recipient},",
                    "casual": "Hi {recipient},"
                },
                "closing_patterns": {
                    "formal": "Sincerely,\n{sender}",
                    "professional": "Best regards,\n{sender}",
                    "casual": "Thanks,\n{sender}"
                }
            },
            
            "report": {
                "structure": ["executive_summary", "background", "analysis", "findings", "recommendations", "conclusion"],
                "section_patterns": {
                    "executive_summary": "This report examines {topic} and provides {analysis_type} for {stakeholders}.",
                    "background": "The context for this analysis includes {background_info} and {current_situation}.",
                    "findings": "Our analysis reveals {key_findings} with {confidence_level} confidence."
                }
            },
            
            "documentation": {
                "structure": ["overview", "requirements", "implementation", "examples", "troubleshooting"],
                "section_patterns": {
                    "overview": "This documentation covers {topic} and provides {guidance_type} for {users}.",
                    "requirements": "Before proceeding, ensure you have {prerequisites} and {dependencies}.",
                    "implementation": "Follow these steps to {objective}: {step_by_step}"
                }
            }
        }
    
    def _initialize_optimization_patterns(self):
        """Initialize content optimization patterns."""
        
        self.optimization_patterns = {
            "readability": {
                "short_sentences": r'\.[\s]+[A-Z]',
                "active_voice": ["is", "are", "was", "were"],
                "transition_words": ["however", "therefore", "furthermore", "moreover", "consequently"]
            },
            
            "engagement": {
                "questions": r'\?',
                "personal_pronouns": ["you", "your", "we", "our"],
                "power_words": ["discover", "proven", "essential", "ultimate", "comprehensive"]
            },
            
            "seo": {
                "keyword_density": 0.02,  # 2% target
                "header_structure": ["h1", "h2", "h3"],
                "meta_elements": ["title", "description", "keywords"]
            }
        }
    
    async def generate_title_and_outline(
        self,
        topic: str,
        content_type: str = "blog_post",
        target_audience: str = "general",
        research: bool = True
    ) -> Tuple[str, List[str]]:
        """
        Generate compelling title and detailed outline.
        
        Args:
            topic: Main topic or subject
            content_type: Type of content to create
            target_audience: Intended audience
            research: Whether to conduct research
            
        Returns:
            Tuple[str, List[str]]: (title, outline)
        """
        
        # Conduct research if requested
        research_result = None
        if research and self.config["web_research_enabled"]:
            research_result = await self.conduct_web_research(topic)
        
        # Generate title options
        titles = self._generate_title_options(topic, content_type, target_audience, research_result)
        
        # Select best title (simplified scoring)
        best_title = max(titles, key=lambda t: self._score_title(t, topic))
        
        # Generate detailed outline
        outline = self._generate_content_outline(topic, content_type, best_title, research_result)
        
        return best_title, outline
    
    def _generate_title_options(
        self,
        topic: str,
        content_type: str,
        audience: str,
        research: Optional[ResearchResult]
    ) -> List[str]:
        """Generate multiple title options."""
        
        titles = []
        
        # Basic title patterns
        title_patterns = {
            "blog_post": [
                f"The Complete Guide to {topic}",
                f"How {topic} Can Transform Your {audience} Strategy",
                f"Understanding {topic}: A Comprehensive Overview",
                f"The Future of {topic}: Trends and Insights",
                f"{topic} Best Practices for {audience}"
            ],
            "report": [
                f"{topic} Analysis Report",
                f"Comprehensive Study of {topic}",
                f"{topic}: Current State and Future Outlook",
                f"Strategic Analysis: {topic} in Modern Context"
            ],
            "documentation": [
                f"{topic} Documentation Guide",
                f"How to Implement {topic}",
                f"{topic}: Setup and Configuration",
                f"Getting Started with {topic}"
            ]
        }
        
        base_titles = title_patterns.get(content_type, title_patterns["blog_post"])
        
        # Enhance with research insights
        if research and research.key_findings:
            research_enhanced = [
                f"{topic}: {finding}" for finding in research.key_findings[:2]
            ]
            titles.extend(research_enhanced)
        
        titles.extend(base_titles)
        return titles[:5]  # Return top 5 options
    
    def _score_title(self, title: str, topic: str) -> float:
        """Score title quality based on multiple factors."""
        
        score = 0.0
        
        # Length optimization (8-60 characters ideal)
        length = len(title)
        if 8 <= length <= 60:
            score += 0.3
        elif length > 60:
            score -= 0.1
        
        # Keyword presence
        if topic.lower() in title.lower():
            score += 0.4
        
        # Power words
        power_words = ["guide", "complete", "ultimate", "comprehensive", "essential", "proven"]
        power_word_count = sum(1 for word in power_words if word in title.lower())
        score += power_word_count * 0.1
        
        # Numbers (tend to perform well)
        if any(char.isdigit() for char in title):
            score += 0.2
        
        return score
    
    def _generate_content_outline(
        self,
        topic: str,
        content_type: str,
        title: str,
        research: Optional[ResearchResult]
    ) -> List[str]:
        """Generate detailed content outline."""
        
        template = self.templates.get(content_type, self.templates["blog_post"])
        base_structure = template["structure"]
        
        outline = []
        
        for section in base_structure:
            section_title = self._generate_section_title(section, topic, research)
            outline.append(section_title)
            
            # Add sub-points for main sections
            if section in ["main_points", "analysis", "implementation"]:
                sub_points = self._generate_sub_points(section, topic, research)
                outline.extend([f"  - {point}" for point in sub_points])
        
        return outline
    
    def _generate_section_title(self, section: str, topic: str, research: Optional[ResearchResult]) -> str:
        """Generate section title based on content structure."""
        
        section_titles = {
            "introduction": f"Introduction to {topic}",
            "main_points": f"Key Aspects of {topic}",
            "examples": f"Real-World Applications of {topic}",
            "conclusion": f"Conclusion and Next Steps",
            "executive_summary": "Executive Summary",
            "background": "Background and Context",
            "analysis": f"Analysis of {topic}",
            "findings": "Key Findings",
            "recommendations": "Recommendations",
            "overview": f"Overview of {topic}",
            "requirements": "Requirements and Prerequisites",
            "implementation": "Implementation Guide",
            "troubleshooting": "Troubleshooting and FAQ"
        }
        
        return section_titles.get(section, f"{section.replace('_', ' ').title()}")
    
    def _generate_sub_points(self, section: str, topic: str, research: Optional[ResearchResult]) -> List[str]:
        """Generate sub-points for outline sections."""
        
        sub_points = {
            "main_points": [
                f"Definition and core concepts of {topic}",
                f"Benefits and advantages",
                f"Common challenges and solutions",
                f"Best practices and recommendations"
            ],
            "analysis": [
                "Current market trends",
                "Comparative analysis",
                "Impact assessment",
                "Future projections"
            ],
            "implementation": [
                "Planning and preparation",
                "Step-by-step process",
                "Tools and resources",
                "Monitoring and evaluation"
            ]
        }
        
        base_points = sub_points.get(section, [])
        
        # Enhance with research findings
        if research and research.key_findings:
            research_points = [f"Research insight: {finding}" for finding in research.key_findings[:2]]
            base_points.extend(research_points)
        
        return base_points[:4]  # Limit to 4 sub-points
    
    async def conduct_web_research(
        self,
        query: str,
        max_sources: int = None
    ) -> ResearchResult:
        """
        Conduct comprehensive web research on a topic.
        
        Args:
            query: Research query
            max_sources: Maximum number of sources to analyze
            
        Returns:
            ResearchResult: Comprehensive research findings
        """
        
        max_sources = max_sources or self.config["max_research_sources"]
        
        # Check cache first
        cache_key = f"research_{query.lower().replace(' ', '_')}"
        if cache_key in self.research_cache:
            cached_result = self.research_cache[cache_key]
            # Check if cache is still valid (1 hour)
            cache_time = datetime.fromisoformat(cached_result.research_timestamp)
            if (datetime.now() - cache_time).seconds < 3600:
                return cached_result
        
        try:
            # Conduct web search
            search_response = await self.api_framework.search_web(query, max_sources)
            
            if not search_response.success:
                return self._create_empty_research_result(query)
            
            # Analyze search results (mock implementation)
            sources = self._extract_sources_from_search(search_response.data, max_sources)
            key_findings = self._extract_key_findings(sources, query)
            citations = self._generate_citations(sources)
            confidence_score = self._calculate_research_confidence(sources, key_findings)
            
            research_result = ResearchResult(
                query=query,
                sources=sources,
                key_findings=key_findings,
                citations=citations,
                confidence_score=confidence_score,
                research_timestamp=datetime.now().isoformat()
            )
            
            # Cache result
            self.research_cache[cache_key] = research_result
            
            return research_result
            
        except Exception as e:
            print(f"Research error: {str(e)}")
            return self._create_empty_research_result(query)
    
    def _create_empty_research_result(self, query: str) -> ResearchResult:
        """Create empty research result for error cases."""
        
        return ResearchResult(
            query=query,
            sources=[],
            key_findings=[],
            citations=[],
            confidence_score=0.0,
            research_timestamp=datetime.now().isoformat()
        )
    
    def _extract_sources_from_search(self, search_data: Any, max_sources: int) -> List[Dict[str, Any]]:
        """Extract and format sources from search results."""
        
        # Mock sources for demonstration
        mock_sources = [
            {
                "title": f"Research Article on {search_data.get('query', 'Topic')}",
                "url": "https://example.com/article1",
                "snippet": "Comprehensive analysis of the topic with detailed insights and practical applications.",
                "source_type": "article",
                "credibility_score": 0.8
            },
            {
                "title": f"Industry Report: {search_data.get('query', 'Topic')} Trends",
                "url": "https://example.com/report1",
                "snippet": "Latest industry trends and future outlook with statistical analysis.",
                "source_type": "report",
                "credibility_score": 0.9
            },
            {
                "title": f"Academic Paper on {search_data.get('query', 'Topic')}",
                "url": "https://example.com/paper1",
                "snippet": "Peer-reviewed research with empirical findings and theoretical framework.",
                "source_type": "academic",
                "credibility_score": 0.95
            }
        ]
        
        return mock_sources[:max_sources]
    
    def _extract_key_findings(self, sources: List[Dict[str, Any]], query: str) -> List[str]:
        """Extract key findings from research sources."""
        
        # Mock key findings based on sources
        findings = []
        
        for source in sources:
            if source["source_type"] == "academic":
                findings.append(f"Academic research shows significant impact of {query} on industry outcomes")
            elif source["source_type"] == "report":
                findings.append(f"Industry trends indicate growing adoption of {query} practices")
            else:
                findings.append(f"Practical applications of {query} demonstrate measurable benefits")
        
        # Add synthesized insights
        if len(sources) > 1:
            findings.append(f"Cross-source analysis reveals {query} as a key factor in modern strategies")
        
        return findings[:5]  # Limit to 5 key findings
    
    def _generate_citations(self, sources: List[Dict[str, Any]]) -> List[str]:
        """Generate properly formatted citations."""
        
        citations = []
        
        for i, source in enumerate(sources, 1):
            citation = f"[{i}] {source['title']}. Retrieved from {source['url']}"
            citations.append(citation)
        
        return citations
    
    def _calculate_research_confidence(self, sources: List[Dict[str, Any]], findings: List[str]) -> float:
        """Calculate confidence score for research results."""
        
        if not sources:
            return 0.0
        
        # Base confidence on source credibility
        avg_credibility = sum(source.get("credibility_score", 0.5) for source in sources) / len(sources)
        
        # Adjust for number of sources
        source_factor = min(len(sources) / 5, 1.0)  # Max boost for 5+ sources
        
        # Adjust for number of findings
        finding_factor = min(len(findings) / 3, 1.0)  # Max boost for 3+ findings
        
        confidence = avg_credibility * 0.6 + source_factor * 0.2 + finding_factor * 0.2
        
        return round(confidence, 2)
    
    async def generate_content(
        self,
        topic: str,
        specifications: ContentSpecification,
        research_results: Optional[ResearchResult] = None
    ) -> GeneratedContent:
        """
        Generate comprehensive content based on specifications.
        
        Args:
            topic: Content topic
            specifications: Detailed content requirements
            research_results: Optional research to incorporate
            
        Returns:
            GeneratedContent: Complete generated content
        """
        
        # Generate title and outline if not provided
        title, outline = await self.generate_title_and_outline(
            topic, 
            specifications.content_type,
            specifications.target_audience,
            specifications.research_requirements
        )
        
        # Conduct research if needed and not provided
        if specifications.research_requirements and not research_results:
            research_results = await self.conduct_web_research(topic)
        
        # Generate content sections
        content_sections = []
        
        for section in outline:
            if section.startswith("  -"):  # Skip sub-points for now
                continue
            
            section_content = await self._generate_section_content(
                section, topic, specifications, research_results
            )
            content_sections.append(section_content)
        
        # Combine content
        full_content = "\n\n".join(content_sections)
        
        # Add citations if required
        if specifications.include_citations and research_results and research_results.citations:
            full_content += "\n\n## References\n\n"
            full_content += "\n".join(research_results.citations)
        
        # Calculate quality score
        quality_score = self._calculate_content_quality(full_content, specifications)
        
        # Create content object
        content_id = f"content_{int(datetime.now().timestamp())}"
        generated_content = GeneratedContent(
            content_id=content_id,
            title=title,
            content=full_content,
            outline=outline,
            word_count=len(full_content.split()),
            specifications=specifications,
            research_used=research_results,
            quality_score=quality_score,
            generation_timestamp=datetime.now().isoformat()
        )
        
        # Store content
        self.generated_content[content_id] = generated_content
        
        return generated_content
    
    async def _generate_section_content(
        self,
        section_title: str,
        topic: str,
        specifications: ContentSpecification,
        research: Optional[ResearchResult]
    ) -> str:
        """Generate content for a specific section."""
        
        # Determine target length per section
        total_length = self.config["length_options"][specifications.length]
        section_length = total_length["min"] // 4  # Rough estimate per section
        
        # Generate section content based on type
        if "introduction" in section_title.lower():
            content = self._generate_introduction(topic, specifications, research)
        elif "conclusion" in section_title.lower():
            content = self._generate_conclusion(topic, specifications, research)
        elif "background" in section_title.lower():
            content = self._generate_background(topic, specifications, research)
        else:
            content = self._generate_main_section(section_title, topic, specifications, research)
        
        # Format section
        formatted_content = f"## {section_title}\n\n{content}"
        
        return formatted_content
    
    def _generate_introduction(
        self,
        topic: str,
        specifications: ContentSpecification,
        research: Optional[ResearchResult]
    ) -> str:
        """Generate introduction section."""
        
        intro_templates = self.templates[specifications.content_type].get("intro_patterns", [])
        
        if intro_templates:
            template = intro_templates[0]  # Use first template
            intro = template.format(
                topic=topic,
                context=specifications.target_audience,
                reason="its proven impact on business outcomes",
                promise="provide comprehensive insights and practical guidance",
                domain=topic.split()[0] if topic.split() else "industry",
                impact="opportunity for growth and innovation"
            )
        else:
            intro = f"This comprehensive analysis of {topic} is designed for {specifications.target_audience}. "
            intro += f"Understanding {topic} is crucial for modern organizations seeking competitive advantage."
        
        # Add research insights if available
        if research and research.key_findings:
            intro += f"\n\nRecent research has revealed {research.key_findings[0].lower()}."
        
        return intro
    
    def _generate_conclusion(
        self,
        topic: str,
        specifications: ContentSpecification,
        research: Optional[ResearchResult]
    ) -> str:
        """Generate conclusion section."""
        
        conclusion_templates = self.templates[specifications.content_type].get("conclusion_patterns", [])
        
        if conclusion_templates:
            template = conclusion_templates[0]
            conclusion = template.format(
                topic=topic,
                benefits="significant advantages",
                audience=specifications.target_audience,
                action="implement these strategies systematically",
                outcome="success",
                strategies="approaches",
                concepts="principles",
                domain=topic.split()[0] if topic.split() else "field"
            )
        else:
            conclusion = f"In conclusion, {topic} represents a valuable opportunity for {specifications.target_audience}. "
            conclusion += "The key to success lies in understanding the fundamentals and implementing best practices."
        
        # Add forward-looking statement
        conclusion += f"\n\nAs {topic} continues to evolve, staying informed about latest developments will be essential for maintaining competitive advantage."
        
        return conclusion
    
    def _generate_background(
        self,
        topic: str,
        specifications: ContentSpecification,
        research: Optional[ResearchResult]
    ) -> str:
        """Generate background section."""
        
        background = f"The field of {topic} has evolved significantly over recent years. "
        background += f"For {specifications.target_audience}, understanding this evolution is crucial for making informed decisions."
        
        if research and research.key_findings:
            background += f"\n\nCurrent research indicates {research.key_findings[0].lower()}. "
            background += "This context shapes how organizations approach implementation and strategy."
        
        return background
    
    def _generate_main_section(
        self,
        section_title: str,
        topic: str,
        specifications: ContentSpecification,
        research: Optional[ResearchResult]
    ) -> str:
        """Generate main content section."""
        
        content = f"When examining {section_title.lower()}, several key factors emerge as particularly important for {specifications.target_audience}.\n\n"
        
        # Add structured content points
        points = [
            f"Understanding the core principles of {topic} enables better decision-making.",
            f"Implementation strategies must align with organizational goals and capabilities.",
            f"Best practices emerge from successful real-world applications and proven methodologies.",
            f"Continuous monitoring and adaptation ensure long-term success and value creation."
        ]
        
        for i, point in enumerate(points, 1):
            content += f"{i}. {point}\n\n"
        
        # Add research insights if available
        if research and research.key_findings:
            relevant_finding = research.key_findings[0] if research.key_findings else ""
            if relevant_finding:
                content += f"Research supports this approach, showing that {relevant_finding.lower()}."
        
        return content
    
    def _calculate_content_quality(self, content: str, specifications: ContentSpecification) -> float:
        """Calculate content quality score."""
        
        score = 0.0
        
        # Length appropriateness
        word_count = len(content.split())
        target_range = self.config["length_options"][specifications.length]
        
        if target_range["min"] <= word_count <= target_range["max"]:
            score += 0.3
        elif word_count < target_range["min"]:
            score += 0.1
        
        # Structure quality (headers, paragraphs)
        headers = len(re.findall(r'^##', content, re.MULTILINE))
        if headers >= 3:
            score += 0.2
        
        # Readability (sentence length, complexity)
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if 10 <= avg_sentence_length <= 20:  # Optimal range
            score += 0.2
        
        # Content depth (keywords, concepts)
        topic_mentions = content.lower().count(specifications.content_type.lower())
        if topic_mentions >= 3:
            score += 0.2
        
        # Professional tone indicators
        professional_indicators = ["analysis", "research", "findings", "conclusions", "recommendations"]
        professional_count = sum(1 for indicator in professional_indicators if indicator in content.lower())
        score += min(professional_count * 0.02, 0.1)
        
        return min(score, 1.0)