# Agent to Agent (A2A) Foundations

This is a beginner-friendly repository demonstrating how to build multi-agent AI systems using the [Agent2Agent (A2A)](https://a2aprotocol.ai/) protocol.

## What is the A2A Protocol?

The Agent2Agent (A2A) protocol is an open standard introduced that addresses a critical challenge in the AI landscape: enabling AI agents built on diverse frameworks by different companies running on separate servers to communicate and collaborate effectively.

A2A provides a standardized way for agents to:

- **Discover each other's capabilities** through "Agent Cards" in JSON format
- **Communicate and collaborate** across different platforms and frameworks
- **Securely exchange information** and coordinate actions
- **Support long-running tasks** with real-time feedback and state updates
- **Handle various modalities** including text, audio, and video streaming

## Project Structure

This repository contains a simple implementation of the A2A protocol:

- `agent.py`: Defines a basic A2A agent that returns "Hello World"
- `server.py`: Implements an A2A server that exposes the agent's capabilities
- `client.py`: Implements an A2A client that can communicate with the server
- `pyproject.toml`: Defines the project dependencies

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/a2a-101.git
cd a2a-101

# Install dependencies
poetry install
```

### Running the Server

```bash
python server.py
```

This will start the A2A server on http://localhost:9999.

### Running the Client

```bash
python client.py
```

This will connect to the server and allow you to interact with the agent.

## Resources

- [A2A Protocol Official Website](https://a2aprotocol.ai/)
- [A2A Protocol GitHub Repository](https://github.com/a2aproject/A2A)
- [A2A Protocol Documentation](https://a2aprotocol.ai/docs/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
