from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

from crewai import Agent, Task, Crew

def setup_output_directory():
    """Create output directory if it doesn't exist"""
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    return output_dir

def save_results(result, output_dir):
    """Save results to a timestamped file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'moon_facts_{timestamp}.txt'
    
    # Convert result to string if it's a CrewOutput object
    result_str = str(result) if hasattr(result, '__str__') else result
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Moon Facts Research\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result_str)
    
    return output_file

def main():
    # Set up output directory
    output_dir = setup_output_directory()
    
    # Define an agent
    agent = Agent(
        role='Senior Astronomer',
        goal='Find and present fascinating facts about the Moon',
        backstory=(
            'You are an expert astronomer with decades of experience studying celestial bodies. '
            'You have a talent for explaining complex astronomical concepts in an engaging and '
            'understandable way.'
        )
    )

    # Define a task for the agent
    moon_task = Task(
        description=(
            'Research and present three particularly interesting and lesser-known facts about the Moon. '
            'For each fact, provide sufficient context to explain why it is significant. '
            'Format the output with clear headings and proper spacing for readability.'
        ),
        expected_output=(
            'A well-structured document with three sections, each containing a different '
            'interesting fact about the Moon. Each section should have a clear heading, '
            'the fact itself, and 2-3 sentences of explanation about why this fact is '
            'notable or surprising.'
        ),
        agent=agent
    )

    # Create a crew with the agent and the task
    crew = Crew(
        agents=[agent],
        tasks=[moon_task],
        verbose=True  # Enable more detailed output
    )

    print("🚀 Starting Moon Facts Research Crew...")
    print("🔍 Researching interesting facts about the Moon...\n")
    
    # Run the crew
    result = crew.kickoff()
    
    # Print the results
    print("\n" + "="*80)
    print("🌕 MOON FACTS RESEARCH RESULTS")
    print("="*80)
    print(result)
    
    # Save the results to a file
    output_file = save_results(result, output_dir)
    print("\n" + "-"*80)
    print(f"📄 Results saved to: {output_file}")
    print("-"*80)

if __name__ == '__main__':
    main()