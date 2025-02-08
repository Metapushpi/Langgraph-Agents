# AI Router with Azure OpenAI

An intelligent routing system that uses Azure OpenAI to process and route user queries to appropriate functions based on intent detection. The system includes persistent memory management and conversation history tracking.

## Project Structure 
project_root/
├── .env # Environment variables and configuration
├── requirements.txt # Python dependencies
├── agent.py # Main AI router implementation
├── api_functions.py # Function implementations for different intents
├── memory_manager.py # Memory management system
├── main.py # Application entry point
├── conversation_history.json # Persistent storage for conversations
└── README.md # Project documentation

## Features

- Intent detection using Azure OpenAI
- Function routing based on detected intent
- Persistent conversation history
- Short-term and long-term memory management
- Search functionality for past conversations
- Support for multiple query types:
  - Financial data queries
  - Weather information
  - News updates
  - Sentiment analysis
  - Language translation

## Prerequisites

1. Python 3.9 or higher
2. Azure OpenAI API access
3. Required environment variables in `.env`:
   ```
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_MODEL_DEPLOYMENT=your_deployment
   AZURE_OPENAI_MODEL_NAME=gpt-35-turbo
   AZURE_OPENAI_API_VERSION=2023-03-15-preview
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd ai-router
   ```

2. Create a virtual environment:
   ```bash
   conda create -n agent python=3.9
   conda activate agent
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Available commands:
   - `exit`: Quit the program
   - `help`: Show help message
   - `history`: Show recent conversations
   - `clear`: Clear conversation history
   - `search <intent>`: Search conversations by intent
   - `context`: Show current conversation context

3. Example queries:
   ```
   What is the stock price of Tesla?
   What's the weather like in Tokyo?
   Tell me the latest news about AI
   Analyze the sentiment of 'The product is amazing'
   Translate 'Hello' to French
   ```

## Components

### agent.py
- `IntelligentRouter`: Main class for processing and routing queries
- Handles Azure OpenAI integration
- Intent detection and function routing

### memory_manager.py
- `EnhancedMemory`: Manages conversation history and context
- Combines short-term (buffer) and long-term (persistent) memory
- Provides search and retrieval functionality

### api_functions.py
- Implementation of various functions for different intents
- Handles specific query types (finance, weather, news, etc.)

### main.py
- Application entry point
- Command-line interface
- Error handling and user interaction

## Memory System

The project uses a dual-memory system:
1. Short-term memory: Using LangChain's ConversationBufferMemory
2. Long-term memory: Persistent JSON storage

Features:
- Conversation history tracking
- Context awareness
- Intent-based search
- Entity tracking
- Persistent storage between sessions

## Error Handling

The system includes comprehensive error handling:
- Input validation
- API error handling
- Memory operation error handling
- Graceful degradation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Support

For support, please [pushpendra.official@gmail.com, +91-8560075234]