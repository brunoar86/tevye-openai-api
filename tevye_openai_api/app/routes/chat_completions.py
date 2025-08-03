from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from tevye_openai_api.app.interfaces.chat_completion import ChatCompletionRequest    # noqa: E501
from tevye_openai_api.app.modules.chat_completion import ChatCompletion


router = APIRouter()
chat = ChatCompletion()


@router.post('/chat/completion', tags=['Chat Completion'])
async def chat_completion(input: ChatCompletionRequest,
                          request: Request, response: Response):
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        result = await chat.request(input)

        return JSONResponse(status_code=200, headers=headers, content=result)

    except HTTPException as error:
        return JSONResponse(status_code=error.status_code,
                            content={"detail": error.detail})

    except Exception as error:
        return JSONResponse(status_code=500,
                            content={"detail": error.detail})
