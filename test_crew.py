import os
from crew_enhanced import ResearchCrew

def main():
    # Test with a simple topic
    topic = "quantum computing"
    print(f"Starting test with topic: {topic}")
    
    try:
        # Initialize the research crew
        print("\nInitializing ResearchCrew...")
        crew = ResearchCrew(topic)
        
        # Run the research
        print("\nRunning research...")
        result = crew.run()
        
        # Display results
        print("\nResearch completed!")
        print(f"Result type: {type(result)}")
        if result.get('result'):
            print(f"First 200 chars: {result['result'][:200]}...")
        else:
            print("No result was generated")
        
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Make sure we're in the right directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
