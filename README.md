# SnapStudy Edge

Private AI study companion designed for Snapdragon PCs.

## What it does

Paste lecture notes and choose:

- Summary: key points, definitions/formulas, and likely exam questions.
- Flashcards: exactly 8 concise question/answer cards.
- Quiz: exactly 7 mixed MCQ and short-answer questions with local answer checking.

## Architecture

Student notes -> Streamlit UI -> local OpenAI-compatible GenieX -> QAIRT -> Snapdragon NPU

The app does not require a hosted AI API for its inference path. If GENIEX_BASE_URL points to a remote service, notes are sent to that endpoint. For private material, keep the endpoint local and trusted.

## Run locally

1. Create a Python environment.
2. Install dependencies:

    pip install -r requirements.txt

3. Start your local GenieX OpenAI-compatible server.
4. Run:

    streamlit run app/app.py

## Configuration

GENIEX_BASE_URL defaults to http://127.0.0.1:8000/v1

Optional environment variables:

- GENIEX_BASE_URL
- GENIEX_API_KEY
- GENIEX_MODEL
- GENIEX_TIMEOUT
- SNAPSTUDY_MAX_NOTES_CHARS

The default study-material limit is 50,000 characters.

## Safety and validation

- Pasted study material is treated as untrusted content; embedded instructions are not intended to override the study-assistant task.
- Flashcard output is validated for exactly 8 cards with question and answer fields.
- Quiz output is validated for exactly 7 questions and valid MCQ/short-answer structures.
- Quiz answers are hidden by default and checked locally in the UI.
- For private notes, use a trusted local GenieX endpoint.

Run the application on the target HP Snapdragon PC before reporting performance results. Record actual inference latency, memory usage, and NPU execution. Qualcomm platform/model reference metrics should not be presented as measurements of this application.

## License

Apache License 2.0. See LICENSE.

## Repository

https://github.com/mohith-krishnaa/SnapStudy-Edge
