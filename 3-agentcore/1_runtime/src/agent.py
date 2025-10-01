from strands import Agent, tool
from strands.models import BedrockModel
import argparse
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp
app = BedrockAgentCoreApp()

# --------------------------
# Custom Tool 1: FAQ Tool
# --------------------------
@tool
def faq_tool(question: str) -> str:
    """
    Respond to common tech support questions.
    """
    faq_answers = {
        "how do i reset my password": "To reset your password, go to settings > account > reset password.",
        "how do i connect to wifi": "To connect to WiFi, go to network settings and choose your network.",
        "how do i update the software": "Open the app store and check for available updates under 'My Apps'."
    }
    normalized = question.lower().strip()
    return faq_answers.get(normalized, "Sorry, I don't have an answer to that FAQ.")

# --------------------------
# Custom Tool 2: Device Troubleshooter Tool
# --------------------------
@tool
def device_troubleshooter(issue: str) -> str:
    """
    Guide the user through basic diagnostic steps.
    """
    steps = {
        "not turning on": "Please hold the power button for 10 seconds. If it still doesn't turn on, try charging the device.",
        "screen frozen": "Hold power + volume down button to restart. Check for software updates after reboot.",
        "no sound": "Ensure volume is up, and Bluetooth isn't redirecting audio elsewhere. Test with headphones."
    }
    normalized = issue.lower().strip()
    return steps.get(normalized, "I suggest restarting your device first. If that doesn't help, try a factory reset.")

# --------------------------
# Custom Tool 3: Ticket Logger Tool
# --------------------------
@tool
def ticket_logger(issue_description: str) -> str:
    """
    Simulate logging a support ticket.
    """
    return f"Ticket has been created for: '{issue_description}'. Our team will get back to you within 24 hours."

# --------------------------
# Agent Setup
# --------------------------
model = BedrockModel(
    model_id="anthropic.claude-3-haiku-20240307-v1:0"
)

agent = Agent(
    model=model,
    tools=[faq_tool, device_troubleshooter, ticket_logger],
    system_prompt=(
        "You are a tech support assistant. "
        "You can answer common questions, troubleshoot device problems, and log tickets if the issue isn't resolved."
    )
)

# --------------------------
# Agent Entrypoint
# --------------------------
@app.entrypoint
def strands_agent_bedrock(payload):
    """
    Invoke the tech support agent with a given payload
    """
    user_input = payload.get("prompt")
    response = agent(user_input)
    return response.message['content'][0]['text']

# --------------------------
# CLI Test
# --------------------------
if __name__ == "__main__":
    app.run()
