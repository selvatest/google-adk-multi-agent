from google.adk.agents.llm_agent import Agent

from models import DEFAULT_MODEL
from user_information.agent import user_information_agent
from product_Catalog.agent import product_agent
from checkout.agent import checkout_agent
from payment.agent import payment_agent
from order_summary.agent import orderSummary_agent
from trigger_email.agent import email_agent

root_agent = Agent(
    model=DEFAULT_MODEL,
    name="root_agent",
    description="Main e-commerce order agent that orchestrates user info, product selection, checkout, payment, summary, email and SMS.",
    instruction=(
        "You are the main shopping assistant for an online store.\n"
        "When a new user starts chatting, first greet them politely, briefly explain that you can help "
        "them place an order end-to-end, and then start the flow.\n"
        "Flow:\n"
        "1) Delegate to user_information_agent to collect the user's name, phone, email, and address "
        "and store them in state.\n"
        "2) After user information is collected, delegate to product_agent to let the user choose a "
        "category and item, and store the selected item and price in state.\n"
        "3) Delegate to checkout_agent to build and show an order summary from state and ask the user "
        "to confirm or cancel.\n"
        "4) If the user confirms, delegate to payment_agent to collect card number and CVV, validate "
        "them, and set payment_status in state.\n"
        "5) If payment succeeds, delegate to orderSummary_agent to generate a text summary and PDF, "
        "then to email_agent and sms_agent to notify the user using the data in state.\n"
        "6) If the user cancels at checkout or payment fails, clearly explain that the order was not "
        "completed and offer to restart or adjust the order.\n"
    ),
    sub_agents=[
        user_information_agent,
        product_agent,
        checkout_agent,
        payment_agent,
        orderSummary_agent,
        email_agent
    ],
)