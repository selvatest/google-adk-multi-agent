from google.adk.agents.llm_agent import Agent
from google.adk.platform import uuid
from google.adk.tools.tool_context import ToolContext
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

from models import DEFAULT_MODEL
from trigger_email.agent import email_agent


def order_summary(tool_context: ToolContext) -> str:
    user_name = tool_context.state.get("user:name")
    user_phone = tool_context.state.get("user:phone")
    user_email = tool_context.state.get("user:email")
    user_address = tool_context.state.get("user:address")

    item = tool_context.state.get("cart:item")
    price = tool_context.state.get("cart:price")
    category = tool_context.state.get("cart:category")

    order_id = str(uuid.uuid4())
    expected_delivery_date = "2 days"

    content = (
        f"Dear {user_name}, order #{order_id} is created for the product '{item}' "
        f"in category '{category}'. Total price is {price}. Expected delivery date "
        f"to the address, phone, email '{user_address} {user_phone} {user_email}' is {expected_delivery_date}."
    )

    # Store summary in state for later (PDF/email/SMS)
    tool_context.state["order:summary_text"] = content
    tool_context.state["order:id"] = order_id

    return content


def generate_pdf(content: str, tool_context: ToolContext) -> str:
    """Creates a PDF from the given content and returns the file path."""
    file_path = "./generated_order_summary.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    doc.build([Paragraph(content, styles["BodyText"])])

    # Save path in state so email/SMS agents can use it
    tool_context.state["order:pdf_path"] = file_path

    return file_path

orderSummary_agent = Agent(
    model=DEFAULT_MODEL,
    name='orderSummary_agent',
    description="Generates the final order summary, creates a PDF, and coordinates email/SMS notifications.",
    instruction=(
        "You are the order summary and notification coordinator.\n"
        "Your responsibilities:\n"
        "1) Read user and cart data from state, including user:name, user:email, user:phone, "
        "user:address, cart:category, cart:item, and cart:price.\n"
        "2) Call the `order_summary(tool_context)` tool to build a clear, human-readable summary of the order. "
        "Store the summary and order id in state (for example: order:summary_text, order:id).\n"
        "3) Call `generate_pdf(content, tool_context)` using the summary text to generate a PDF file. "
        "Ensure the PDF path is stored in state (for example: order:pdf_path).\n"
        "4) After the PDF is generated, delegate to the `email_agent` sub-agent to send an email with the "
        "order summary and PDF attachment to the user's email address.\n"
        "5) Then delegate to the `sms_agent` sub-agent to send a short confirmation SMS to the user's phone.\n"
        "6) Finally, respond to the user with a brief confirmation message that:\n"
        "   - Includes the order id.\n"
        "   - States that the email and SMS confirmations have been sent.\n"
        "Do not ask for new user details or payment information here; they should already be present in state."
    ),
    tools=[order_summary, generate_pdf]
)