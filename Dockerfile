FROM python:3.12-slim

WORKDIR /tevye-openai-api

COPY /tevye_openai_api /tevye-openai-api/tevye_openai_api

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tevye-openai-api/tevye_openai_api/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "tevye_openai_api.app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]