"""Task definitions for the research crew."""
from textwrap import dedent
from crewai import Task
from typing import List, Optional
from datetime import datetime
from pathlib import Path
from config import OUTPUT_DIR


class ResearchTasks:
    """Class to manage all research tasks."""
    
    def __init__(self, topic: str):
        """Initialize with the research topic.
        
        Args:
            topic: The research topic
        """
        self.topic = topic
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{topic.lower().replace(' ', '_')}_{self.timestamp}.md"
        self.output_file = OUTPUT_DIR / filename
    
    def research_task(self, agent) -> Task:
        """Create a research task.
        
        Args:
            agent: The agent assigned to this task
            
        Returns:
            Task: Configured research task
        """
        description = (
            f"Research and gather detailed information about {self.topic}. "
            "Focus on finding unique, interesting, and lesser-known facts. "
            "Provide detailed explanations and context for each finding. "
            "Include specific examples, statistics, and sources where possible. "
            "Make sure to cover different aspects and perspectives on the topic."
        )
        
        expected_output = (
            f"A comprehensive research document with detailed findings about "
            f"{self.topic}, including sources and references. "
            "The document should be well-structured and informative."
        )
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            output_file=str(self.output_file)
        )
    
    def fact_check_task(self, agent, context: Optional[List[Task]] = None) -> Task:
        """Create a fact-checking task.
        
        Args:
            agent: The agent assigned to this task
            context: List of tasks that this task depends on
            
        Returns:
            Task: Configured fact-checking task
        """
        description = dedent("""
            Review the research findings and verify their accuracy.
            Check facts against reliable sources and ensure all information is up-to-date.
            Flag any information that cannot be verified.
            Provide sources for your verifications when possible.
        """)
        
        expected_output = dedent("""
            A verified version of the research document with fact-checked 
            information and notes on verification status.
            Include any corrections or additional context needed.
        """)
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            context=context or [],
            output_file=str(self.output_file)
        )
    
    def writing_task(self, agent, context: Optional[List[Task]] = None) -> Task:
        """Create a writing task.
        
        Args:
            agent: The agent assigned to this task
            context: List of tasks that this task depends on
            
        Returns:
            Task: Configured writing task
        """
        description = (
            "Transform the verified research into a well-structured, "
            "engaging article about {topic}. "
            "Use markdown formatting with clear headings and sections. "
            "Ensure the content is accessible to a general audience. "
            "Include an introduction, main content with subsections, and a conclusion."
        ).format(topic=self.topic)
        
        expected_output = (
            "A well-written article about {topic}, formatted in markdown, "
            "with proper sections, headings, and clear explanations. "
            "The article should be informative, engaging, and well-structured."
        ).format(topic=self.topic)
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            context=context or [],
            output_file=str(self.output_file)
        )
