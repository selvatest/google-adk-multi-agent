from google.adk.agents.llm_agent import Agent


import os
import mailtrap as mt
from google.adk.tools.tool_context import ToolContext

from models import DEFAULT_MODEL

MAILTRAP_TOKEN = os.environ["MAILTRAP_API_KEY"]


def send_email(tool_context: ToolContext) -> str:
    # Read summary and order id from state
    summary_text = tool_context.state.get("order:summary_text")
    order_id = tool_context.state.get("order:id")
    user_email = tool_context.state.get("user:email")

    # Fallbacks if missing
    if not summary_text:
        summary_text = "Order summary not found in state."
    if not order_id:
        order_id = "UNKNOWN"
    if not user_email:
        user_email = "mselvakumartest@gmail.com"  # test inbox, or your Mailtrap inbox

    # Build email body
    body = f"Order {order_id}\n\n{summary_text}"

    mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Order Agent"),
        to=[mt.Address(email=user_email)],
        subject=f"Order Confirmation #{order_id}",
        text=body,
        category="Integration Test",
    )

    client = mt.MailtrapClient(token=MAILTRAP_TOKEN)
    response = client.send(mail)

    # You can store status in state for debugging
    tool_context.state["order:email_status"] = str(response)

    return "EMAIL_SENT"

email_agent = Agent(
    model=DEFAULT_MODEL,
    name='email_agent',
    description="Sends the order confirmation email via Mailtrap using the summary and PDF stored in state.",
    instruction=(
        "You are responsible only for sending the order confirmation email.\n"
        "1) Read the summary text and order id from state (for example: order:summary_text and order:id).\n"
        "2) Read the PDF file path from state if available (for example: order:pdf_path).\n"
        "3) Call the `send_email(tool_context)` tool to send an email to the user's email address stored in state.\n"
        "   - The email body should include the order id and the summary text.\n"
        "   - Attach the PDF if the path is available.\n"
        "4) After the tool call succeeds, tell the user that an email confirmation has been sent to their email address.\n"
        "If required data is missing from state, clearly explain what is missing and return control to the calling agent; "
        "do not attempt to collect user information yourself."
    ),
    tools=[send_email],
)