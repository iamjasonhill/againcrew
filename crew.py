"""Crew orchestration for the research project."""
import time
from typing import Dict, Any
from pathlib import Path
from crewai import Crew, Process
from agents import ResearchAgents
from tasks import ResearchTasks
from config import OUTPUT_DIR

class ResearchCrew:
    """Class to manage the research crew and its tasks."""
    
    def __init__(self, topic: str):
        """Initialize the research crew with a topic."""
        self.topic = topic.strip()
        if not self.topic:
            raise ValueError("Research topic cannot be empty")
            
        # Initialize agents and tasks
        self.agents = ResearchAgents()
        self.tasks = ResearchTasks(self.topic)
        
        # Initialize progress tracking
        self.start_time = time.time()
        self.task_progress = {
            'research': {'status': 'pending', 'start_time': None, 'end_time': None},
            'fact_check': {'status': 'pending', 'start_time': None, 'end_time': None},
            'writing': {'status': 'pending', 'start_time': None, 'end_time': None}
        }
    
    def update_progress(self, task_name: str, status: str) -> None:
        """Update the progress of a task."""
        if task_name not in self.task_progress:
            return
            
        if status == 'start':
            self.task_progress[task_name]['status'] = 'in_progress'
            self.task_progress[task_name]['start_time'] = time.time()
        elif status in ['completed', 'failed']:
            self.task_progress[task_name]['status'] = status
            self.task_progress[task_name]['end_time'] = time.time()
    
    def get_progress(self) -> Dict[str, Dict[str, Any]]:
        """Get the current progress of all tasks."""
        return {
            'overall': {
                'status': self._get_overall_status(),
                'elapsed_time': time.time() - self.start_time
            },
            'tasks': self.task_progress
        }
    
    def _get_overall_status(self) -> str:
        """Get the overall status of the research."""
        statuses = [task['status'] for task in self.task_progress.values()]
        
        if 'in_progress' in statuses:
            return 'in_progress'
        if all(status == 'completed' for status in statuses):
            return 'completed'
        if 'failed' in statuses:
            return 'failed'
        return 'pending'
    
    def run(self) -> Dict[str, Any]:
        """Run the research crew and return results."""
        try:
            # Initialize agents
            researcher = self.agents.create_researcher()
            fact_checker = self.agents.create_fact_checker()
            writer = self.agents.create_writer()
            
            # Create tasks with dependencies
            research_task = self.tasks.research_task(researcher)
            fact_check_task = self.tasks.fact_check_task(fact_checker, [research_task])
            write_task = self.tasks.writing_task(writer, [fact_check_task])
            
            # Set up progress tracking callbacks
            for task, task_name in zip(
                [research_task, fact_check_task, write_task],
                ['research', 'fact_check', 'writing']
            ):
                task.callback = lambda status, name=task_name: self.update_progress(name, status)
            
            # Create and run the crew
            crew = Crew(
                agents=[researcher, fact_checker, writer],
                tasks=[research_task, fact_check_task, write_task],
                verbose=True,
                process='sequential'
            )
            
            # Execute the crew
            result = crew.kickoff()
            
            return {
                'topic': self.topic,
                'result': str(result),
                'output_file': self.tasks.output_file,
                'success': True,
                'progress': self.get_progress()
            }
            
        except Exception as e:
            return {
                'topic': self.topic,
                'error': str(e),
                'success': False,
                'progress': self.get_progress()
            }
