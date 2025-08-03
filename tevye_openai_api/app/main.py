from fastapi import FastAPI

from tevye_openai_api.app.routes import health
from tevye_openai_api.app.routes import chat_completions
from tevye_openai_api.app.routes import audio


app = FastAPI(title='OpenAI API', docs_url='/swagger',
              openapi_url='/openapi.json', version='0.3.1')

app.include_router(health.router)
app.include_router(chat_completions.router)
app.include_router(audio.router)
