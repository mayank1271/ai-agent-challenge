# ai-agent-challenge
Agent-as-Coder Challenge: Bank Statement Parser
This project features an autonomous AI agent built with LangGraph and the Groq API. The agent's primary function is to programmatically write, test, and self-correct a Python parser for bank statement PDFs, demonstrating a complete agentic workflow as required by the Karbon AI Challenge.

Agent Workflow Diagram
The agent operates as a state machine, moving between nodes to accomplish its goal. It begins by generating Python code for the parser, which is then saved to a file. This code is immediately validated by a pytest suite that compares its output to a ground-truth CSV. If the test fails, the agent captures the specific error and feeds it back into the generation node, creating a self-correction loop. This cycle repeats for a maximum of three attempts, ensuring the agent either succeeds or fails gracefully.

![image alt](https://github.com/mayank1271/ai-agent-challenge/blob/3fd07c19ba025a5ea8a0610981ee326652ac0ed5/given%20pdf%20(2).png)

How to Run
Follow these 5 steps to run the agent from a fresh clone of this repository.

1. Clone the Repository:

git clone <your-repository-url>
cd ai-agent-challenge

2. Create and Activate a Virtual Environment:

# Create the environment
python -m venv .venv

# Activate it (on Windows)
.venv\Scripts\activate

3. Install Dependencies:

pip install -r requirements.txt

4. Set Up Environment Variables:
Create a file named .env in the root of the project and add your Groq API key:

GROQ_API_KEY="your_api_key_here"

5. Run the Agent:
To run the agent and generate the parser for the ICICI bank statement, execute the following command:

python agent.py --target icici

The agent will then begin its generation and self-correction loop. Upon success, the final, correct parser will be located at custom_parser/
