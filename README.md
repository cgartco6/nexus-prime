# Nexus Prime - AI-Powered Project Orchestration System

Nexus Prime is a sophisticated multi-agent framework that coordinates specialized AI agents to complete complex projects ranging from app development to content creation.

## Features

- **Multi-Agent Architecture**: Coordinates specialized AI agents for different tasks
- **Project Persistence**: Saves project state for resuming work later
- **Task Dependency Management**: Handles complex task dependencies
- **Web Interface**: User-friendly web UI for project management
- **External API Integration**: Connects to image generation, code execution, and deployment services
- **Feedback Loops**: Improves results through iterative refinement

## Installation

1. Clone the repository
2. Run the setup script: `./setup.sh`
3. Copy `.env.example` to `.env` and add your API keys
4. Activate the virtual environment: `source venv/bin/activate`
5. Start the web interface: `python web_interface/app.py`

## Usage

1. Open your browser to `http://localhost:5000`
2. Enter a project description (e.g., "Create a weather dashboard web app")
3. View the generated plan and execute tasks
4. Monitor progress and download generated artifacts

## Agents

- **ProjectSynapse**: Project management and planning
- **CodeWeaver**: Code development and implementation
- **LogicSphere**: Algorithm design and system architecture
- **Q-Arc**: Quality assurance and testing
- **PixelGenius**: UI/UX design and visual assets
- **ScriptSensei**: Content creation and narrative design
- **Aura**: Audio engineering and sound design
- **DataScientist**: Data analysis and machine learning
- **BlockchainDeveloper**: Blockchain and smart contract development
- **DevOpsEngineer**: Infrastructure and deployment automation

## API Integration

Nexus Prime integrates with:
- Stability AI for image generation
- Piston API for code execution
- Netlify for deployment (simulated)

## License

MIT License
