import streamlit as st
from google import genai
from google.genai import types


# ── Single client instance (cached across reruns) ──────────────────────────
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def call_gemini(system_prompt: str, chat_history: list[dict], user_message: str) -> str:
    """
    Calls Gemini 2.5 Flash with proper multi-turn history and a system prompt.

    chat_history: list of {"role": "User" | "AI", "content": "..."}
                  Should NOT include the current user_message (we add it here).
    """
    client = get_client()

    # Build properly typed content history (exclude last item = current user msg)
    contents = []
    for msg in chat_history[:-1]:  # Skip the message we just appended in app.py
        role = "user" if msg["role"] == "User" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])]
            )
        )

    # Append the current user turn
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.85,
                top_p=0.95,
                max_output_tokens=2048,
            ),
        )
        return response.text

    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"