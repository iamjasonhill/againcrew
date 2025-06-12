from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_crewai():
    try:
        # Create a simple agent
        researcher = Agent(
            role='Researcher',
            goal='Research information',
            backstory='You are a helpful assistant',
            verbose=True
        )

        # Create a simple task
        task = Task(
            description='Find information about the moon',
            agent=researcher,
            expected_output='A paragraph about the moon'
        )

        # Create a crew
        crew = Crew(
            agents=[researcher],
            tasks=[task],
            verbose=True
        )

        # Run the crew
        result = crew.kickoff()
        print("\nTest successful! Crew AI is working correctly.")
        print("\nResult:", result)
        return True
        
    except Exception as e:
        print("\nError occurred during test:")
        print(str(e))
        return False

if __name__ == "__main__":
    print("Testing Crew AI setup...")
    success = test_crewai()
    if success:
        print("✅ Crew AI is working correctly!")
    else:
        print("❌ There was an issue with the Crew AI setup.")
