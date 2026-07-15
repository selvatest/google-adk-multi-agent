from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext

from models import DEFAULT_MODEL


def dummy_payment(card_number: str, cvv: str, tool_context: ToolContext) -> dict:
    # Basic length checks
    is_card_valid = len(card_number) == 16 and card_number.isdigit()
    is_cvv_valid = len(cvv) in (3, 4) and cvv.isdigit()

    summary = tool_context.state.get("order:summary", {}) or {}

    if is_card_valid and is_cvv_valid:
        payment_status = "SUCCESS"
    else:
        payment_status = "FAILED"

    # Store payment details in state
    summary["payment_status"] = payment_status
    summary["card_number_masked"] = card_number[-4:]  # last 4 digits only
    summary["cvv_length"] = len(cvv)

    tool_context.state["order:summary"] = summary

    return {
        "payment_status": payment_status,
        "message": (
            "Payment successful." if payment_status == "SUCCESS"
            else "Invalid card number or security code. Please check and try again."
        ),
    }

payment_agent = Agent(
    model=DEFAULT_MODEL,
    name='payment_agent',
    description="Handles payment after checkout confirmation.",
    instruction=(
        "Ask the user for a 16-digit card number and 3 or 4 digit security code. "
        "Call dummy_payment with those values. If payment_status is SUCCESS, "
        "tell the user payment is complete. If FAILED, explain what went wrong "
        "and let them try again."
    ),
    tools=[dummy_payment]
)