# Enhanced CrewAI Research Assistant

This project showcases an enhanced implementation of [CrewAI](https://github.com/joaomdmoura/crewAI) with multiple specialized agents working together to research topics, fact-check information, and generate well-structured reports.

## Features

- **Multi-Agent System**: Uses specialized agents for research, fact-checking, and content writing
- **Interactive Web Interface**: Built with Streamlit for easy interaction
- **Markdown Export**: Save research results as well-formatted Markdown files
- **Fact-Checking**: Includes a dedicated fact-checking agent to verify information
- **Modular Design**: Easy to extend with new agents and tasks

## Setup

1. Create and activate a Python virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your-api-key-here`

## Usage

### Command Line Interface
Run the basic research crew:
```sh
python main.py
```

### Web Interface
Launch the interactive web app:
```sh
streamlit run crew_enhanced.py
```

## Project Structure

- `main.py`: Basic CrewAI implementation (single agent)
- `crew_enhanced.py`: Enhanced implementation with multiple agents and web interface
- `output/`: Directory where research reports are saved
- `requirements.txt`: Project dependencies

## Customization

You can modify the agents, tasks, and prompts in `crew_enhanced.py` to suit your specific needs. The code is well-documented and follows a modular design for easy extension.

## License

This project is open source and available under the [MIT License](LICENSE).