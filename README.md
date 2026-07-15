# E‑Commerce Multi‑Agent Chatbot (Google ADK)

This project is a multi‑agent e‑commerce assistant built with **Google Agent Development Kit (ADK)**.  
It guides a user end‑to‑end through:

1. Collecting user information  
2. Selecting products  
3. Building an order summary  
4. Processing payment (dummy)  
5. Generating an order summary PDF  
6. Sending confirmation email

The project is designed for **ETL / QA automation** learning, with a focus on agent orchestration and LLM‑driven flows.

---

## Project Structure

```text
.
├── models.py                 # DEFAULT_MODEL and related model config
├── .env                      # API keys and provider URLs (not committed)
├── root_agent.py             # Main root_agent definition
├── user_information/
│   └── agent.py              # user_information_agent
├── product_Catalog/
│   └── agent.py              # product_agent
├── checkout/
│   └── agent.py              # checkout_agent
├── payment/
│   └── agent.py              # payment_agent
├── order_summary/
│   └── agent.py              # orderSummary_agent
├── trigger_email/
│   └── agent.py              # email_agent
└── ...
```

Each subfolder contains a dedicated ADK `Agent` responsible for one part of the flow.

---

## Root Agent Flow

The `root_agent` orchestrates the entire conversation:

1. **Greet the user** and explain the flow.
2. **Delegate to `user_information_agent`**  
   - Collects: full name, phone, email, shipping address  
   - Stores details in shared state.
3. **Delegate to `product_agent`**  
   - Helps user select a product category and item  
   - Stores selected item and price in state.
4. **Delegate to `checkout_agent`**  
   - Builds an order summary from state  
   - Asks user to confirm or cancel.
5. **Delegate to `payment_agent`** (on confirm)  
   - Collects dummy card number and CVV  
   - Validates inputs and sets `payment_status` in state.
6. **Delegate to `orderSummary_agent` + `email_agent`** (on success)  
   - Generates a text summary and PDF  
   - Sends confirmation email using data in state.
7. **Handle cancel / failure**  
   - If user cancels or payment fails, clearly explain that the order was not completed  
   - Offer to restart or adjust the order.

---

## LLM Configuration

### 1. Default Model

`models.py` defines the default LLM model used by all agents:

```python
import os

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "models/gemini-1.5-flash")
```

All agents use:

```python
from models import DEFAULT_MODEL

root_agent = Agent(
    model=DEFAULT_MODEL,
    name="root_agent",
    ...
)
```

Sub‑agents also use `DEFAULT_MODEL` so they share the same provider.

### 2. Environment Variables

LLM providers and other services are configured via `.env`:

```env
# Gemini
GOOGLE_GENAI_USE_ENTERPRISE=0
GEMINI_API_BASE=https://generativelanguage.googleapis.com/v1beta
GOOGLE_API_KEY=your-google-api-key

# Ollama (optional, if using local models)
OLLAMA_API_BASE=http://127.0.0.1:11434

# OpenAI (optional)
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://api.openai.com/v1

# Email provider
MAILTRAP_API_KEY=your-mailtrap-key

# Default model for ADK
DEFAULT_MODEL=models/gemini-1.5-flash
```

> Note:  
> OpenCode variables (e.g., `OPENCODE_BASE_URL`, `OPENCODE_API_KEY`) are currently used in **separate PyCharm scripts**, not directly inside ADK.

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# or
.\.venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure Google ADK and any required SDKs (e.g., Mailtrap client, Ollama client) are included in `requirements.txt`.

### 4. Configure `.env`

Create a `.env` in the project root:

```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GEMINI_API_BASE=https://generativelanguage.googleapis.com/v1beta
GOOGLE_API_KEY=your-google-api-key

MAILTRAP_API_KEY=your-mailtrap-key

DEFAULT_MODEL=models/gemini-1.5-flash
```

(Optionally) add:

```env
OLLAMA_API_BASE=http://127.0.0.1:11434
OPENAI_API_KEY=...
OPENAI_API_BASE=https://api.openai.com/v1
OPENCODE_BASE_URL=https://opencode.ai/zen
OPENCODE_API_KEY=...
```

> Keep `.env` out of Git (add it to `.gitignore`).

---

## Running the Agent

You can run the root agent via a small runner script (example):

```python
# run_root_agent.py
from root_agent import root_agent

if __name__ == "__main__":
    # Replace with your ADK run helper (e.g., root_agent.run(), cli runner, or FastAPI handler)
    root_agent.run()
```

Then:

```bash
python run_root_agent.py
```

Depending on your ADK integration:

- You might run via a CLI tool,  
- Or expose the agent via an API endpoint.

---

## Error Handling & Testing Notes

- The system may occasionally receive **`503 UNAVAILABLE`** errors from upstream LLM providers (e.g., Gemini) when demand is high.  
  - These should be handled with retries and user‑friendly messages instead of raw error dumps.
- For automation testing:
  - You can simulate failed LLM calls and verify:
    - The flow stops gracefully.  
    - The user is told the assistant is temporarily unavailable.  
    - No partial order is created on failed payment or checkout.

---


## Future Enhancements

- Add robust retry and fallback logic for 503 errors from LLM providers.  
- Integrate OpenCode via a LiteLLM / OpenAI‑compatible proxy so that ADK can call DeepSeek models transparently.  
- Add ETL validation tests as separate agents (e.g., validating data pipelines or warehouse loading).  

---

If you’re using this project for learning, you can extend it by:

- Adding new sub‑agents (e.g., `sms_agent`).  
- Wiring in ETL validation logic after order creation.  
- Using OpenCode in PyCharm to auto‑generate test cases and then running those tests as part of the agent workflow.
