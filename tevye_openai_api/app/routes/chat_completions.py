from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from tevye_openai_api.app.utils.logger import log
from tevye_openai_api.app.modules.chat_completion import ChatCompletion
from tevye_openai_api.app.interfaces.chat_completion import ChatCompletionRequest    # noqa: E501


router = APIRouter()
chat = ChatCompletion()


@router.post('/chat/completion', tags=['Chat Completion'])
async def chat_completion(input: ChatCompletionRequest,
                          request: Request, response: Response):
    try:
        log.info("Received chat completion request", input=dict(input))
        headers = {
            'Content-Type': 'application/json'
        }
        result = await chat.request(input)
        log.info("Chat completion response", result=result)

        return JSONResponse(status_code=200, headers=headers, content=result)

    except HTTPException as error:
        log.error("HTTPException occurred", status_code=error.status_code,
                  detail=error.detail)
        return JSONResponse(status_code=error.status_code,
                            content={"detail": error.detail})

    except Exception as error:
        log.error("Unexpected error occurred", error=str(error))
        return JSONResponse(status_code=500,
                            content={"detail": error.args[0]})
