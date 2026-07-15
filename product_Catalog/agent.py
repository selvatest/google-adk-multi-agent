
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext

from models import DEFAULT_MODEL


def product_Catalog(tool_context: ToolContext):
    categories = ["electronics", "medicine", "home appliances", "furniture", "office"]
    # store available categories in state (optional)
    tool_context.state["cart:categories"] = categories
    return categories

def item(category: str, tool_context: ToolContext):
    if category == "electronics":
        items = ["google pixel", "motorola", "iphone"]
    elif category == "medicine":
        items = ["ointment", "pain killer", "tylenol"]
    elif category == "home appliances":
        items = ["washing machine", "refrigerator", "stove"]
    elif category == "furniture":
        items = ["chair", "table", "stool"]
    elif category == "office":
        items = ["notebook", "pen", "stapler"]
    else:
        items = ["unknown"]

    tool_context.state["cart:category"] = category
    tool_context.state["cart:items"] = items
    return items

def price(item_name: str, tool_context: ToolContext):
    prices = {
        "google pixel": 1100,
        "motorola": 500,
        "iphone": 1000,
        "ointment": 1000,
        "pain killer": 10,
        "tylenol": 10,
        "washing machine": 2000,
        "refrigerator": 3000,
        "stove": 1000,
        "chair": 150,
        "table": 589,
        "stool": 888,
        "notebook": 90,
        "pen": 20,
        "stapler": 12,
    }
    item_price=prices.get(item_name, None)

    tool_context.state["cart:item_price"] = item_price
    tool_context.state["cart:item_name"] = item_name

    return item_price

product_agent = Agent(
    model=DEFAULT_MODEL,
    name="product_agent",
    description="Product catalog and pricing agent.",
    instruction=(
        "You are responsible only for product selection and pricing.\n"
        "Behavior:\n"
        "1) First, call the `product_Catalog(tool_context)` tool to get the list of available categories "
        "from state (cart:categories).\n"
        "2) Then ask the user which category they are interested in, using exactly these categories: \n"
        " call product_Catalog(tool_context) \n"
        "3) When the user answers with one of these categories, call `item(category, tool_context)` to list items in that category.\n"
        "4) Present the items in a clear list and ask the user which item they want.\n"
        "5) When the user chooses an item, call `price(item_name, tool_context)` to get the price and tell the user the exact item and price.\n"
        "6) After you have confirmed the chosen item and price with the user, stop and wait for the main agent "
        "to move to checkout. Do not talk about payment or shipping; that belongs to other agents."
    ),
    tools=[product_Catalog, item, price],
)