from google.adk import Agent
from google.adk.tools.tool_context import ToolContext

from models import DEFAULT_MODEL
from payment.agent import payment_agent


def build_checkout_summary(tool_context: ToolContext) -> dict:
    # Read all needed fields from state
    user_name = tool_context.state.get("user:name")
    user_email = tool_context.state.get("user:email")
    user_phone = tool_context.state.get("user:phone")
    user_address = tool_context.state.get("user:address")

    category = tool_context.state.get("cart:category")
    item_name = tool_context.state.get("cart:item")
    price = tool_context.state.get("cart:price")

    summary = {
        "user_name": user_name,
        "user_email": user_email,
        "user_phone": user_phone,
        "user_address": user_address,
        "category": category,
        "item": item_name,
        "price": price,
    }

    # Store summary in state for payment/PDF later
    tool_context.state["order:summary"] = summary

    return summary

checkout_agent = Agent(
    model=DEFAULT_MODEL,
    name='checkout_agent',
    description="Builds checkout summary and asks for confirmation.",
    instruction=(
         "You are responsible only for the checkout confirmation step.\n"
        "1) Read user information and cart data from state (user:name, user:email, user:phone, user:address, "
        "cart:category, cart:item, cart:price).\n"
        "2) Call the `build_checkout_summary` tool to construct a clear summary of the order.\n"
        "3) Show this summary to the user and explicitly ask: 'Do you want to confirm this order? (yes/no)'.\n"
        "4) If the user says 'yes', respond with a brief confirmation and say that you will now proceed to payment, "
        "then return control to the main agent.\n"
        "5) If the user says 'no' or cancels, clearly state that the order was not confirmed and the flow should return "
        "to product selection or end, depending on the main agent's policy.\n"
        "Do not collect card details here; payment_agent will handle that."
    ),
    tools=[build_checkout_summary]
)