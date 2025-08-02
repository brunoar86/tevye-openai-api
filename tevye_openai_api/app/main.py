from fastapi import FastAPI

from tevye_openai_api.app.routes import health
from tevye_openai_api.app.routes import index


app = FastAPI(title='OpenAI API', docs_url='/swagger',
              openapi_url='/openapi.json', version='0.1.0')

app.include_router(health.router)
app.include_router(index.router)
