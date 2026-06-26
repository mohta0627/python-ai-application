# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the app
python3 -m streamlit run app.py
```

## API Key Setup

The app resolves the Gemini API key in this priority order (`utils/gemini_client.py`):

1. `.streamlit/secrets.toml` — `GEMINI_API_KEY = "..."` (persistent, preferred)
2. Sidebar UI input — stored in `st.session_state["gemini_api_key"]` for the session

Copy `.streamlit/secrets.toml.example` → `.streamlit/secrets.toml` and fill in the key to avoid entering it on every run.

## Architecture

All generation flows through a single path: `app.py` collects user inputs → calls a prompt builder in `utils/prompts.py` → passes the resulting string to `utils/gemini_client.generate()` → renders the returned text with `st.markdown`.

**`utils/prompts.py`** — one function per tool, each returning a plain string prompt. All prompts are in Japanese and target Japanese output. The function signatures directly mirror the UI controls in `app.py`.

**`utils/gemini_client.py`** — `generate(prompt)` is the only public function. It calls `get_client()` on every invocation (no singleton), which configures `google.generativeai` and returns a `GenerativeModel("gemini-2.0-flash")`.

**`app.py`** — single-file Streamlit app. Tool selection is a `selectbox`; each tool is an `if/elif` branch that renders its own UI and calls the corresponding prompt function. No pages, no session state beyond the API key.

## Adding a New Tool

1. Add a prompt function to `utils/prompts.py`.
2. Add the tool label to the `selectbox` list in `app.py`.
3. Add an `elif` branch in `app.py` that collects inputs, calls the prompt function, and passes it to `generate()`.
