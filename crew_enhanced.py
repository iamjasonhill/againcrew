import os
import streamlit as st
import time
from typing import Dict, List, Optional, Any
from crewai.process import Process

# Set page config first (must be the first Streamlit command after import)
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from typing import Dict, List, Optional, Any
import json
import time
from streamlit_chat import message as st_message

# Custom CSS for chat interface
st.markdown("""
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    max-width: 80%;
    word-wrap: break-word;
}
.chat-message.user {
    background-color: #2b313e;
    margin-left: auto;
    border-bottom-right-radius: 0;
}
.chat-message.assistant {
    background-color: #4a4a4a;
    margin-right: auto;
    border-bottom-left-radius: 0;
}
.stButton>button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

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
        print(f"\n{'='*50}\nInitializing ResearchCrew with topic: {topic}\n{'='*50}")
        self.topic = topic.strip()
        if not self.topic:
            raise ValueError("Research topic cannot be empty")
            
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.start_time = time.time()
        self.task_progress = {
            'research': {'status': 'pending', 'start_time': None, 'end_time': None},
            'fact_check': {'status': 'pending', 'start_time': None, 'end_time': None},
            'writing': {'status': 'pending', 'start_time': None, 'end_time': None}
        }
        self.current_task = None
        
        print("\n🔧 Initializing agents...")
        self._initialize_agents()
        print("✅ Agents initialized successfully")
        
    def _initialize_agents(self):
        """Initialize all agents with error handling"""
        try:
            self._initialize_researcher()
            self._initialize_fact_checker()
            self._initialize_writer()
        except Exception as e:
            print(f"❌ Error initializing agents: {str(e)}")
            raise
        
    def _initialize_researcher(self):
        """Initialize the researcher agent"""
        print("  - Initializing Researcher agent...")
        self.researcher = Agent(
            role='Senior Research Analyst',
            goal=f'Find and analyze interesting information about {self.topic}',
            backstory=(
                'You are an expert researcher with a talent for finding '
                'fascinating and accurate information on any topic. You have '
                'a keen eye for detail and a passion for sharing knowledge.'
            ),
            verbose=True,
            allow_delegation=False
        )
        print("    ✅ Researcher agent ready")
    
    def _initialize_fact_checker(self):
        """Initialize the fact checker agent"""
        print("  - Initializing Fact Checker agent...")
        self.fact_checker = Agent(
            role='Fact Checker',
            goal='Verify the accuracy of research findings',
            backstory=(
                'You are a meticulous fact-checker with a background in '
                'journalism and research. You ensure all information is '
                'accurate, up-to-date, and properly sourced.'
            ),
            verbose=True,
            allow_delegation=False
        )
        print("    ✅ Fact Checker agent ready")
    
    def _initialize_writer(self):
        """Initialize the writer agent"""
        print("  - Initializing Writer agent...")
        self.writer = Agent(
            role='Content Writer',
            goal='Create engaging and well-structured content',
            backstory=(
                'You are a talented writer who specializes in making complex '
                'information accessible and engaging for a broad audience.'
            ),
            verbose=True,
            allow_delegation=False
        )
        print("    ✅ Writer agent ready")
    
    def update_progress(self, task_name: str, status: str):
        """Update the progress of a task"""
        if task_name in self.task_progress:
            self.task_progress[task_name]['status'] = status
            if status == 'in_progress':
                self.task_progress[task_name]['start_time'] = time.time()
                self.current_task = task_name
            elif status == 'completed':
                self.task_progress[task_name]['end_time'] = time.time()
                self.current_task = None
    
    def get_progress(self) -> Dict:
        """Get current progress information"""
        completed = sum(1 for t in self.task_progress.values() if t['status'] == 'completed')
        total = len(self.task_progress)
        progress = (completed / total) if total > 0 else 0
        
        current_task = next((k for k, v in self.task_progress.items() 
                            if v['status'] == 'in_progress'), None)
        
        return {
            'progress': progress * 100,
            'completed': completed,
            'total': total,
            'current_task': current_task,
            'task_details': self.task_progress
        }
    
    def create_tasks(self) -> List[Task]:
        """Create tasks for the research crew"""
        print("\n🛠️  Creating research task...")
        research_task = Task(
            description=(
                f'Research and gather detailed information about {self.topic}.\n'
                'Focus on finding unique, interesting, and lesser-known facts.\n'
                'Provide detailed explanations and context for each finding.\n'
                'Include specific examples, statistics, and sources where possible.'
            ),
            agent=self.researcher,
            expected_output=(
                'A comprehensive research document with detailed findings about '
                f'{self.topic}, including sources and references.\n'
                'The document should be well-structured and informative.'
            )
        )
        print("✅ Research task created")
        
        print("\n🛠️  Creating fact-checking task...")
        fact_check_task = Task(
            description=(
                'Review the research findings and verify their accuracy.\n'
                'Check facts against reliable sources and ensure all information is up-to-date.\n'
                'Flag any information that cannot be verified.\n'
                'Provide sources for your verifications when possible.'
            ),
            agent=self.fact_checker,
            expected_output=(
                'A verified version of the research document with fact-checked '
                'information and notes on verification status.\n'
                'Include any corrections or additional context needed.'
            ),
            context=[research_task]
        )
        print("✅ Fact-checking task created")
        
        print("\n🛠️  Creating writing task...")
        output_path = f'output/{self.topic.lower().replace(" ", "_")}_{self.timestamp}.md'
        write_task = Task(
            description=(
                'Transform the verified research into a well-structured, '
                'engaging article.\n'
                'Use markdown formatting with clear headings and sections.\n'
                'Ensure the content is accessible to a general audience.\n'
                'Include an introduction, main content with subsections, and a conclusion.'
            ),
            agent=self.writer,
            expected_output=(
                'A well-written article about the topic, formatted in markdown, '
                'with proper sections, headings, and clear explanations.\n'
                'The article should be informative, engaging, and well-structured.'
            ),
            context=[fact_check_task],
            output_file=output_path
        )
        print(f"✅ Writing task created. Output will be saved to: {output_path}")
        
        return [research_task, fact_check_task, write_task]
    
    def run(self) -> Dict:
        """Run the research crew and return results"""
        print(f"\n{'='*50}\nStarting research on: {self.topic}\n{'='*50}")
        try:
            # Create tasks with error handling
            print("\n🛠️  Creating tasks...")
            try:
                tasks = self.create_tasks()
                if not tasks or len(tasks) == 0:
                    raise ValueError("No tasks were created")
                print(f"✅ Created {len(tasks)} tasks")
            except Exception as e:
                print(f"❌ Error creating tasks: {str(e)}")
                raise
            
            # Set up task progress callbacks
            print("\n🔄 Setting up task callbacks...")
            try:
                for i, task in enumerate(tasks):
                    task_name = ['research', 'fact_check', 'writing'][i]
                    print(f"  - Setting up callback for {task_name} task")
                    task.callback = lambda status, task_name=task_name, i=i: [
                        print(f"\n📡 Callback for {task_name} task: {status}"),
                        self.update_progress(
                            task_name,
                            'in_progress' if status == 'start' else 'completed'
                        )
                    ][-1]
            except Exception as e:
                print(f"❌ Error setting up task callbacks: {str(e)}")
                raise
            
            # Initialize crew
            print("\n🤖 Initializing crew...")
            try:
                crew = Crew(
                    agents=[self.researcher, self.fact_checker, self.writer],
                    tasks=tasks,
                    verbose=True,
                    process='sequential'  # Changed from Process.SEQUENTIAL to string 'sequential'
                )
                print("✅ Crew initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing crew: {str(e)}")
                raise
            
            # Execute crew
            print(f"\n🚀 Starting research execution...")
            try:
                result = crew.kickoff()
                print(f"\n✅ Research execution completed")
                print(f"Result type: {type(result)}")
                if result:
                    print(f"First 200 chars: {str(result)[:200]}...")
                else:
                    print("⚠️ Warning: Empty result from crew.kickoff()")
            except Exception as e:
                print(f"❌ Error during crew execution: {str(e)}")
                # Try to get partial results if available
                if hasattr(crew, 'intermediate_steps'):
                    print("\n🔍 Intermediate steps:")
                    for i, step in enumerate(crew.intermediate_steps or []):
                        print(f"  Step {i+1}: {str(step)[:200]}...")
                raise
            
            # Ensure output directory exists
            self.output_dir.mkdir(exist_ok=True)
            
            # Create output file
            output_file = self.output_dir / f"{self.topic.lower().replace(' ', '_')}_{self.timestamp}.md"
            output_file_str = ""
            
            if not result:
                print("⚠️ Warning: Empty result from crew.kickoff()")
                result = "No content was generated. This might be due to an issue with the agents or task setup."
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(str(result))
                output_file_str = str(output_file)
                print(f"📄 Output written to: {output_file}")
            except Exception as e:
                print(f"⚠️ Warning: Could not write to output file: {e}")
                output_file_str = ""
            
            return {
                'topic': self.topic,
                'timestamp': self.timestamp,
                'result': result,
                'output_file': output_file_str,
                'progress': self.get_progress(),
                'success': True
            }
            
        except Exception as e:
            print(f"❌ Error in ResearchCrew.run(): {str(e)}")
            return {
                'topic': self.topic,
                'error': str(e),
                'success': False
            }

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI research assistant. What would you like to learn about today?"}
        ]
    if 'research_in_progress' not in st.session_state:
        st.session_state.research_in_progress = False
    if 'research_result' not in st.session_state:
        st.session_state.research_result = None

def display_chat():
    """Display chat messages"""
    st.title("🔍 AI Research Assistant")
    
    # Display chat messages
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def process_research(topic: str):
    """Process research request"""
    try:
        # Initialize progress bar and status
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_ui(progress_data):
            """Update the UI with current progress"""
            progress = progress_data.get('progress', 0)
            current_task = progress_data.get('current_task', 'Starting...')
            
            # Update progress bar
            progress_bar.progress(int(progress))
            
            # Update status text
            task_descriptions = {
                'research': '🔍 Researching information...',
                'fact_check': '✅ Verifying facts...',
                'writing': '✍️  Writing report...'
            }
            
            status_text.markdown(f"""
            **Progress:** {int(progress)}%  
            **Status:** {task_descriptions.get(current_task, 'Starting research...')}
            """)
        
        # Initialize crew and get initial progress
        crew = ResearchCrew(topic)
        update_ui(crew.get_progress())
        
        # Start research in a background thread
        import threading
        result = {}
        
        def run_crew():
            nonlocal result
            result = crew.run()
            st.session_state.research_result = result
        
        thread = threading.Thread(target=run_crew)
        thread.start()
        
        # Update UI while research is in progress
        while thread.is_alive():
            update_ui(crew.get_progress())
            time.sleep(0.5)
        
        # Final update
        update_ui({'progress': 100, 'current_task': 'completed'})
        
        # Read and return the research result
        output_file = result.get('output_file', '')
        if output_file and os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    return f"# Research Complete: {topic}\n\n{f.read()}"
            except Exception as e:
                return f"❌ Error reading research results: {str(e)}"
        else:
            # If no file was created, return the result directly
            return f"# Research Complete: {topic}\n\n{result.get('result', 'No content was generated.')}"
    except Exception as e:
        return f"❌ An error occurred during research: {str(e)}"

def main():
    """Main function to run the enhanced Crew AI application"""
    initialize_session_state()
    
    # Display chat messages
    display_chat()
    
    # Chat input
    if prompt := st.chat_input("Type your research topic or question..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Process the research
        response = process_research(prompt)
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update the chat display
        st.rerun()
    
    # Display research result if available
    if st.session_state.get('research_result'):
        with st.sidebar:
            st.header("Research Results")
            with open(st.session_state.research_result['output_file'], 'r') as f:
                content = f.read()
                st.download_button(
                    label="📥 Download Report",
                    data=content,
                    file_name=f"{st.session_state.research_result['topic'].lower().replace(' ', '_')}_report.md",
                    mime="text/markdown"
                )
    
    # Add some helpful examples in the sidebar
    with st.sidebar:
        st.header("💡 Try these examples")
        examples = [
            "Tell me about quantum computing",
            "What are the latest advancements in AI?",
            "Explain how blockchain works"
        ]
        for example in examples:
            if st.button(example, key=f"example_{example}"):
                st.session_state.messages.append({"role": "user", "content": example})
                response = process_research(example)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

if __name__ == '__main__':
    if not st.session_state.get('show_results', False):
        st.session_state.show_results = False
    main()
