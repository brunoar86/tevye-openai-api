# Tevye OpenAI API

API built with [FastAPI](https://fastapi.tiangolo.com/) to provide endpoints for health checks, chat completions, and audio (speech-to-text and text-to-speech) features, inspired by OpenAI's API.

## Features

- **Health Check Endpoints**: Liveness and readiness routes for monitoring.
- **Chat Completions**: Endpoint for chat-based AI completions.
- **Audio**:
  - Upload `.mp3` files.
  - Speech-to-text transcription using OpenAI Whisper.
  - Text-to-speech synthesis.

## Project Structure

```
tevye-openai-api/
├── tevye_openai_api/
│   ├── app/
│   │   ├── main.py                # FastAPI app and router includes
│   │   ├── routes/
│   │   │   ├── health.py          # Health check endpoints
│   │   │   ├── chat_completions.py# Chat completions endpoints
│   │   │   ├── audio.py           # Audio endpoints (upload, transcription, TTS)
│   │   ├── modules/
│   │   │   └── stt/
│   │   │       ├── speech_to_text.py # Speech-to-text logic
│   │   │       └── mp3/           # Uploaded mp3 files
│   ├── __main__.py                # Entrypoint for running with `python -m`
├── README.md
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/brunoar86/tevye-openai-api.git
   cd tevye-openai-api
   ```

2. **Create a virtual environment and activate:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

### Via Uvicorn

```bash
uvicorn tevye_openai_api.app.main:app --reload
```

### Via Python module

```bash
python -m tevye_openai_api
```

## Usage

- **Swagger UI:** [http://localhost:8000/swagger](http://localhost:8000/swagger)
- **OpenAPI Spec:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

### Example: Uploading an MP3 file

```bash
curl -X POST "http://localhost:8000/audio/upload" \
  -F "file=@/path/to/your/file.mp3"
```

### Example: Transcribing Audio

```bash
curl -X POST "http://localhost:8000/audio/transcriptions" \
  -F "file=@/path/to/your/file.mp3" \
  -F "model=whisper-1" \
  -F "language=English"
```

## Environment Variables

Configure your OpenAI credentials and other secrets as environment variables or in a `.env` file if supported.

- `OPENAI_API_KEY`
- `OPENAI_PROJECT_ID`
- `OPENAI_ORGANIZATION_ID`

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.