from fastapi import APIRouter, Request, Response, Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from tevye_openai_api.app.interfaces.text_to_speech import TTSRequest
from tevye_openai_api.app.interfaces.speech_to_text import STTRequest
from tevye_openai_api.app.modules.tts.text_to_speech import TextToSpeech
from tevye_openai_api.app.modules.stt.speech_to_text import SpeechToText

tts = TextToSpeech()
stt = SpeechToText()
router = APIRouter()


@router.post('/audio/speech', tags=['Audio'])
async def text_to_speech(input: TTSRequest,
                         request: Request, response: Response):
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        result = await tts.request(input)

        return JSONResponse(status_code=200, headers=headers, content=result)

    except HTTPException as error:
        return JSONResponse(status_code=error.status_code,
                            content={"detail": error.detail})

    except Exception as error:
        return JSONResponse(status_code=500, content=error)


@router.post('/audio/upload', tags=['Audio'])
async def upload_audio(request: Request, response: Response,
                       file: UploadFile = File(...),
                       file_name: str = Form(...)):
    try:
        import os
        import shutil

        save_dir = 'tevye_openai_api/app/modules/stt/mp3/'
        os. makedirs(save_dir, exist_ok=True)
        file_name = file_name + '.mp3'
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        headers = {
            'Content-Type': 'application/json'
        }

        message = {'file': file_name, 'status': 'File uploaded successfully'}

        return JSONResponse(status_code=200, headers=headers, content=message)

    except Exception as error:
        return JSONResponse(status_code=500, content=error)


@router.post('/audio/transcriptions', tags=['Audio'])
async def speech_to_text(request: Request, response: Response,
                         input: STTRequest):
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        result = await stt.request(input)

        return JSONResponse(status_code=200, headers=headers, content=result)

    except HTTPException as error:
        return JSONResponse(status_code=error.status_code,
                            content={"detail": error.detail})

    except Exception as error:
        return JSONResponse(status_code=500, content=error)
