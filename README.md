# SnapStudy Edge

Private AI study companion designed for Snapdragon PCs.

## What it does

Paste lecture notes and choose:

- Summary: key points, definitions/formulas, and likely exam questions.
- Flashcards: 8 concise question/answer cards.
- Quiz: 7 mixed MCQ and short-answer questions.

## Architecture

Student notes -> Streamlit UI -> local OpenAI-compatible GenieX -> QAIRT -> Snapdragon NPU

The app does not require a hosted AI API for its inference path.

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

Default model name:

Llama-v3.2-3B-Instruct-SSD

## Validation

Run the application on the target HP Snapdragon PC before reporting performance results. Record actual inference latency, memory usage, and NPU execution. Qualcomm platform/model reference metrics should not be presented as measurements of this application.

## Repository

https://github.com/mohith-krishnaa/SnapStudy-Edge
