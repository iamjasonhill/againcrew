import os
import streamlit as st
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from typing import Dict, List, Optional
import json

# Set page config first (must be the first Streamlit command)
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Set OpenAI API key from Streamlit secrets or environment
if 'OPENAI_API_KEY' in st.secrets:
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
elif 'OPENAI_API_KEY' in os.environ:
    pass  # Use the environment variable if it exists
else:
    st.error('Please set OPENAI_API_KEY in Streamlit secrets or environment variables')
    st.stop()

# Configure ChromaDB with the new client API
try:
    import chromadb
    
    # Initialize the new Chroma client
    chroma_client = chromadb.PersistentClient(
        path=".chroma_cache",  # Directory to store the database
        settings=chromadb.Settings(
            anonymized_telemetry=False  # Disable telemetry
        )
    )
    
    # Test the connection
    chroma_client.heartbeat()
    
except ImportError:
    st.warning("ChromaDB not installed. Some features may be limited.")
    chroma_client = None
except Exception as e:
    st.warning(f"Failed to initialize ChromaDB: {str(e)}. Some features may be limited.")
    chroma_client = None

class ResearchCrew:
    def __init__(self, topic: str):
        self.topic = topic
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Initialize agents
        self.researcher = Agent(
            role='Senior Research Analyst',
            goal=f'Find and analyze interesting information about {topic}',
            backstory=(
                'You are an expert researcher with a talent for finding '
                'fascinating and accurate information on any topic. You have '
                'a keen eye for detail and a passion for sharing knowledge.'
            ),
            verbose=True
        )
        
        self.fact_checker = Agent(
            role='Fact Checker',
            goal='Verify the accuracy of research findings',
            backstory=(
                'You are a meticulous fact-checker with a background in '
                'journalism and research. You ensure all information is '
                'accurate, up-to-date, and properly sourced.'
            ),
            verbose=True
        )
        
        self.writer = Agent(
            role='Content Writer',
            goal='Create engaging and well-structured content',
            backstory=(
                'You are a talented writer who specializes in making complex '
                'information accessible and engaging for a broad audience.'
            ),
            verbose=True
        )
    
    def create_tasks(self) -> List[Task]:
        """Create tasks for the research crew"""
        research_task = Task(
            description=(
                f'Research and gather detailed information about {self.topic}.\n'
                'Focus on finding unique, interesting, and lesser-known facts.\n'
                'Provide detailed explanations and context for each finding.'
            ),
            agent=self.researcher,
            expected_output=(
                'A comprehensive research document with detailed findings about '
                f'{self.topic}, including sources and references.'
            )
        )
        
        fact_check_task = Task(
            description=(
                'Review the research findings and verify their accuracy.\n'
                'Check facts against reliable sources and ensure all information is up-to-date.\n'
                'Flag any information that cannot be verified.'
            ),
            agent=self.fact_checker,
            expected_output=(
                'A verified version of the research document with fact-checked '
                'information and notes on verification status.'
            ),
            context=[research_task]
        )
        
        write_task = Task(
            description=(
                'Transform the verified research into a well-structured, '
                'engaging article.\n'
                'Use markdown formatting with clear headings and sections.\n'
                'Ensure the content is accessible to a general audience.'
            ),
            agent=self.writer,
            expected_output=(
                'A well-written article about the topic, formatted in markdown, '
                'with proper sections, headings, and clear explanations.'
            ),
            context=[fact_check_task],
            output_file=f'output/{self.topic.lower().replace(" ", "_")}_{self.timestamp}.md'
        )
        
        return [research_task, fact_check_task, write_task]
    
    def run(self) -> Dict:
        """Run the research crew and return results"""
        tasks = self.create_tasks()
        
        crew = Crew(
            agents=[self.researcher, self.fact_checker, self.writer],
            tasks=tasks,
            verbose=True  # Set to True for detailed output
        )
        
        print(f"🚀 Starting research on: {self.topic}")
        result = crew.kickoff()
        
        return {
            'topic': self.topic,
            'timestamp': self.timestamp,
            'result': result,
            'output_file': f'output/{self.topic.lower().replace(" ", "_")}_{self.timestamp}.md'
        }

def main():
    """Main function to run the enhanced Crew AI application"""
    st.title("🔍 AI Research Assistant")
    st.write("Enter a topic to research and get detailed, fact-checked information.")
    
    with st.sidebar:
        st.header("Research Settings")
        topic = st.text_input("Enter a research topic:", "The Moon")
        
        if st.button("Start Research"):
            with st.spinner(f"Researching {topic}..."):
                try:
                    crew = ResearchCrew(topic)
                    result = crew.run()
                    
                    st.session_state.research_result = result
                    st.session_state.show_results = True
                    
                    st.success("Research completed successfully!")
                    
                    # Display the result
                    with open(result['output_file'], 'r') as f:
                        content = f.read()
                        st.download_button(
                            label="Download Report",
                            data=content,
                            file_name=f"{topic.lower().replace(' ', '_')}_report.md",
                            mime="text/markdown"
                        )
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    if st.session_state.get('show_results', False):
        st.header(f"Research Results: {st.session_state.research_result['topic']}")
        
        with open(st.session_state.research_result['output_file'], 'r') as f:
            content = f.read()
            st.markdown(content)

if __name__ == '__main__':
    if not st.session_state.get('show_results', False):
        st.session_state.show_results = False
    main()
