from dotenv import load_dotenv
import os
load_dotenv()

from crewai import Agent, Task, Crew

# Define an agent
agent = Agent(
    role='Researcher',
    goal='Find interesting facts about the Moon',
    backstory='You are an expert astronomer who loves sharing knowledge about space.'
)

# Define a task for the agent, and assign the agent
moon_task = Task(
    description='Research and summarize three interesting facts about the Moon.',
    expected_output='A short summary with three facts about the Moon.',
    agent=agent
)

# Create a crew with the agent and the task
crew = Crew(
    agents=[agent],
    tasks=[moon_task]
)

if __name__ == '__main__':
    result = crew.kickoff()
    print('CrewAI Result:')
    print(result) 