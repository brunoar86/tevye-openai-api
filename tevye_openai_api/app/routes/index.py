from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from tevye_openai_api.app.interfaces.chat_completion import ChatCompletionRequest    # noqa: E501
from tevye_openai_api.app.interfaces.text_to_speech import TTSRequest
from tevye_openai_api.app.modules.chat_completion import ChatCompletion
from tevye_openai_api.app.modules.tts.text_to_speech import TextToSpeech

router = APIRouter()
chat = ChatCompletion()
tts = TextToSpeech()


@router.post('/chat/completion', tags=['Chat Completion'])
async def chat_completion(input: ChatCompletionRequest,
                          request: Request, response: Response):
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        result = await chat.request(input)

        return JSONResponse(status_code=200, headers=headers, content=result)

    except Exception as error:
        return JSONResponse(status_code=500, content=error)


@router.post('/audio/speech', tags=['Audio'])
async def text_to_speech(input: TTSRequest,
                         request: Request, response: Response):
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        result = await tts.request(input)

        return JSONResponse(status_code=200, headers=headers, content=result)

    except Exception as error:
        return JSONResponse(status_code=500, content=error)
