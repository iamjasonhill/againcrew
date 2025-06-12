"""Agent definitions for the research crew."""
from textwrap import dedent
from crewai import Agent
from langchain_openai import ChatOpenAI
from config import (
    DEFAULT_LLM, 
    DEFAULT_TEMPERATURE,
    DEFAULT_VERBOSE,
    DEFAULT_ALLOW_DELEGATION
)

class ResearchAgents:
    """Class to manage all research agents."""
    
    def __init__(self):
        """Initialize the LLM for the agents."""
        self.llm = ChatOpenAI(
            model_name=DEFAULT_LLM,
            temperature=DEFAULT_TEMPERATURE,
        )
    
    def create_researcher(self) -> Agent:
        """Create a researcher agent."""
        return Agent(
            role='Senior Research Analyst',
            goal='Find and analyze interesting information on given topics',
            backstory=dedent("""
                You are an expert researcher with a talent for finding fascinating 
                and accurate information on any topic. You have a keen eye for detail 
                and a passion for sharing knowledge. Your research is thorough and 
                well-documented, with proper sources and citations.
            """),
            verbose=DEFAULT_VERBOSE,
            allow_delegation=DEFAULT_ALLOW_DELEGATION,
            llm=self.llm
        )
    
    def create_fact_checker(self) -> Agent:
        """Create a fact checker agent."""
        return Agent(
            role='Fact Checker',
            goal='Verify the accuracy of research findings',
            backstory=dedent("""
                You are a meticulous fact-checker with a background in journalism 
                and research. You ensure all information is accurate, up-to-date, 
                and properly sourced. You have a keen eye for detail and a commitment 
                to truth and accuracy.
            """),
            verbose=DEFAULT_VERBOSE,
            allow_delegation=DEFAULT_ALLOW_DELEGATION,
            llm=self.llm
        )
    
    def create_writer(self) -> Agent:
        """Create a content writer agent."""
        return Agent(
            role='Content Writer',
            goal='Create engaging and well-structured content',
            backstory=dedent("""
                You are a talented writer who specializes in making complex 
                information accessible and engaging for a broad audience. Your writing 
                is clear, concise, and compelling, with a focus on delivering value 
                to the reader.
            """),
            verbose=DEFAULT_VERBOSE,
            allow_delegation=DEFAULT_ALLOW_DELEGATION,
            llm=self.llm
        )
