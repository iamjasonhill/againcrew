"""Main entry point for the Crew AI Research Assistant."""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add the current directory to the Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

from crew import ResearchCrew
from config import OUTPUT_DIR


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run AI research assistant')
    parser.add_argument(
        '--topic',
        type=str,
        default='artificial intelligence',
        help='Research topic (default: artificial intelligence)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=OUTPUT_DIR,
        help=f'Output directory (default: {OUTPUT_DIR})'
    )
    return parser.parse_args()


def main():
    """Main function to run the research crew."""
    args = parse_arguments()
    
    print(f"🚀 Starting research on: {args.topic}")
    print(f"📁 Output directory: {args.output_dir}")
    
    try:
        # Initialize and run the research crew
        research_crew = ResearchCrew(args.topic)
        result = research_crew.run()
        
        if result.get('success', False):
            print(f"\n✅ Research completed successfully!")
            print(f"📄 Output file: {result.get('output_file')}")
            print("\n" + "="*80)
            print(result['result'][:500] + "...")
            print("="*80 + "\n")
            print("✨ Research complete! Check the output file for the full results.")
        else:
            print(f"\n❌ Research failed with error: {result.get('error')}")
            
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        if os.getenv('DEBUG', '').lower() == 'true':
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()