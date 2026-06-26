from google import genai
import streamlit as st


def get_api_key():
    return st.secrets.get("GEMINI_API_KEY") or st.session_state.get("gemini_api_key")


def generate(prompt: str) -> str:
    api_key = get_api_key()
    if not api_key:
        st.error("Gemini APIキーが設定されていません。サイドバーから入力してください。")
        return ""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text
