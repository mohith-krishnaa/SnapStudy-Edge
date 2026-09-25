import json
import os
import re
from typing import Any

import requests
import streamlit as st

st.set_page_config(page_title="SnapStudy Edge", page_icon="SnapStudy", layout="wide")

GENIEX_BASE_URL = os.getenv("GENIEX_BASE_URL", "http://127.0.0.1:8000/v1")
GENIEX_API_KEY = os.getenv("GENIEX_API_KEY", "local")
GENIEX_MODEL = os.getenv("GENIEX_MODEL", "Llama-v3.2-3B-Instruct-SSD")
REQUEST_TIMEOUT = int(os.getenv("GENIEX_TIMEOUT", "120"))


def call_local_model(system_prompt: str, user_prompt: str) -> str:
    url = f"{GENIEX_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GENIEX_API_KEY}",
    }
    payload = {
        "model": GENIEX_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("GenieX returned an unexpected response format.") from exc


def extract_json_text: str) -> Any:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}|\[.*\]", cleaned, flags=re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def build_summary(notes: str) -> str:
    return call_local_model(
        """You are a precise study assistant. Work only from the supplied notes.
Do not invent facts. Return concise Markdown with:
1) 5-8 key points
2) important definitions/formulas
3) likely exam questions.""",
        notes,
    )


def build_flashcards(notes: str) -> list[dict[str, Any]]:
    result = call_local_model(
        """Create exactly 8 concise flashcards from the supplied study material.
Return ONLY a JSON array of objects with keys "question" and "answer".
Do not add facts that are not supported by the notes.""",
        notes,
    )
    cards = extract_json(result)
    if not isinstance(cards, list):
        raise RuntimeError("Flashcard response was not a JSON array.")
    return cards


def build_quiz(notes: str) -> dict[str, Any]:
    result = call_local_model(
        """Create exactly 7 mixed study questions from the supplied notes.
Return ONLY JSON with this shape:
{
  "questions": [
    {
      "type": "mcq" or "short_answer",
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "..."
    }
  ]
}
Keep answers concise and grounded in the notes.""",
        notes,
    )
    quiz = extract_json(result)
    if not isinstance(quiz, dict) or not isinstance(quiz.get("questions"), list):
        raise RuntimeError("Quiz response was not in the expected JSON format.")
    return quiz


def render_flashcards(cards: list[dict[str, Any]]) -> None:
    for index, card in enumerate(cards, start=1):
        with st.expander(f"Card {index}: {card.get('question', 'Question')}"):
            st.write(card.get("answer", ""))


def render_quiz(quiz: dict[str, Any]) -> None:
    questions = quiz.get("questions", [])
    for index, item in enumerate(questions, start=1):
        st.markdown(f"**{index}. {item.get('question', '')}**")
        if item.get("type") == "mcq":
            options = item.get("options", [])
            st.radio(
                "Choose an answer",
                options,
                key=f"quiz_{index}",
                label_visibility="collapsed",
            )
        else:
            st.text_input("Your answer", key=f"quiz_{index}", label_visibility="collapsed")

    st.divider()
    st.caption("Answer key")
    for index, item in enumerate(questions, start=1):
        st.write(f"{index}. {item.get('answer', '')}")


st.title("SnapStudy SnapStudy Edge")
st.caption("Private AI study companion designed for local Snapdragon inference")

with st.sidebar:
    st.subheader("Local inference")
    st.code(GENIEX_BASE_URL, language="text")
    st.write(f"Model: {GENIEX_MODEL}")
    st.info(
        "Study material is sent to the configured local GenieX endpoint. "
        "This UI does not require a hosted AI API."
    )

notes = st.text_area(
    "Paste your lecture notes",
    height=330,
    placeholder="Paste a chapter, class notes, formulas, or revision material here...",
)

mode = st.radio("Study action", ["Summary", "Flashcards", "Quiz"], horizontal=True)
generate = st.button("Generate", type="primary", use_container_width=True)

if generate:
    if not notes.strip():
        st.warning("Paste some study material first.")
    else:
        with st.spinner("Running local inference..."):
            try:
                if mode == "Summary":
                    st.markdown(build_summary(notes))
                elif mode == "Flashcards":
                    render_flashcards(build_flashcards(notes))
                else:
                    render_quiz(build_quiz(notes))
            except requests.RequestException as exc:
                st.error(
                    "Could not reach GenieX. Start the local OpenAI-compatible "
                    f"server and verify GENIEX_BASE_URL. Details: {exc}"
                )
            except (RuntimeError, json.JSONDecodeError) as exc:
                st.error(f"Model response could not be processed: {exc}")

st.divider()
st.caption(
    "SnapStudy Edge  Streamlit UI -> GenieX -> QAIRT -> Snapdragon NPU. "
    "Record real device measurements before claiming application performance."
)
