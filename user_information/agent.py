from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import  ToolContext

from models import DEFAULT_MODEL


def user_information(
    name: str,
    phone: str,
    email: str,
    address: str,
    tool_context: ToolContext,
):
    user_data = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
    }

    # Store in state (session-level working memory)
    tool_context.state["user:name"] = name
    tool_context.state["user:phone"] = phone
    tool_context.state["user:email"] = email
    tool_context.state["user:address"] = address
    tool_context.state["user:profile"] = user_data

    return user_data

user_information_agent = Agent(
    model=DEFAULT_MODEL,
    name='user_information_agent',
    description="Collects user information (name, phone, email, address) and stores it in state for later steps.",
    instruction=(
        "You are responsible for collecting the user's basic contact and shipping information.\n"
        "1) Greet the user politely and explain that you need their details to place the order.\n"
        "2) Ask for the following fields one by one:\n"
        "   - Full name.\n"
        "   - Phone number.\n"
        "   - Email address.\n"
        "   - Shipping address.\n"
        "3) After you have received all four values, call the `user_information` tool to store them in state "
        "(user:name, user:phone, user:email, user:address).\n"
        "4) Confirm back to the user what you stored (repeat their name, email, phone, and address) and say that "
        "the system will now move to product selection.\n"
        "Do not recommend products or discuss payment here; your only job is to collect and store user information."
    ),
    tools=[user_information],
)