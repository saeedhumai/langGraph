# LangGraph Chat Bot

A conversational AI application built with LangGraph and OpenAI's GPT models, featuring graph-based state management and conversation flow.

## Setup

1. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install Dependencies**

```bash
pip install openai>=1.0.0 python-dotenv langgraph
```

3. **Environment Configuration**
   Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Project Structure

```
langgraph/
├── app/
│   ├── config.py          # Environment configuration
│   ├── llm/
│   │   └── llmconfig.py   # OpenAI client setup
│   └── schema/
│       └── schema.py      # State management
├── main.py                # Main application
├── .env                   # API keys (not in git)
└── README.md
```

## Usage

Run the application:

```bash
python main.py
```

- Type your message when prompted with "User: "
- Type 'quit', 'exit', or 'q' to end chat
- Conversation graph is saved in `graphs/` directory

## Features

- Interactive chat with GPT-4/3.5
- Graph-based conversation flow
- Automatic message handling
- Graph visualization export
- Environment variable configuration

## Requirements

- Python 3.12+
- OpenAI API key
- Dependencies listed in setup section
