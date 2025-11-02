# AI Monitoring Agent

## Features
- Tracks competitor/news topics online
- Summarizes articles weekly using GPT-4
- Saves output to text file (can be emailed or pushed to dashboard)
- Conceptual agent can be expanded with Slack/Notion integration

## Setup
1. Create virtual environment using below commands
   `python -m venv venv`
   `venv\Scripts\activate`
2. Install dependencies:
pip install -r requirements.txt
3. Add OpenAI API key in `config.py`.
4. Run:
python agent_workflow.py