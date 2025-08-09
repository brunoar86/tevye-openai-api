import os
import aiohttp
import structlog

from fastapi import HTTPException

from tevye_openai_api.app.settings.openai import project

log = structlog.get_logger(__name__='text_to_speech module')


class TextToSpeech:

    def __init__(self):
        self.OPENAI_API_KEY = project.key()
        self.PROJECT_ID = project.id()
        self.ORGANIZATION_ID = project.organization()
        self.input = None
        self.mp3_path = 'tevye_openai_api/app/modules/tts/mp3/speech.mp3'

    def assemble_request(self):
        log.debug("Assembling TTS request", input=dict(self.input))
        url = 'https://api.openai.com/v1/audio/speech'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.OPENAI_API_KEY),
            'OpenAI-Project': self.PROJECT_ID,
            'OpenAI-Organization': self.ORGANIZATION_ID
        }

        payload = {}

        for k, v in dict(self.input).items():
            if k not in payload and v is not None:
                payload[str(k)] = v

        req = {
            'url': url,
            'headers': headers,
            'payload': payload
        }

        log.debug("Assembled TTS request", req=req['payload'])
        return req

    async def request(self, input):

        self.input = input

        req = self.assemble_request()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=req['url'], headers=req['headers'],
                                        json=req['payload']) as response:
                    log.debug("TTS request sent", status=response.status)
                    if response.status == 200:
                        content = await response.read()
                        os.makedirs(os.path.dirname(self.mp3_path),
                                    exist_ok=True)
                        with open(self.mp3_path, 'wb') as file:
                            file.write(content)
                        log.info("TTS response received",
                                 file_path=self.mp3_path)

                        return self.mp3_path

                    elif response.status == 400:
                        response = await response.json()
                        log.error("TTS request failed",
                                  status_code=response.status,
                                  response=response['error']['message'])
                        raise HTTPException(status_code=response.status,
                                            detail=response['error']['message']
                                            )

                    else:
                        response = await response.json()
                        log.error("TTS request failed",
                                  status_code=response.status,
                                  response=response['error']['message'])
                        raise HTTPException(status_code=response.status,
                                            detail=response['error']['message']
                                            )

            except aiohttp.ClientError as error:
                log.error("TTS request failed due to client error",
                          error=str(error))
                raise HTTPException(status_code=500,
                                    detail="TTS request failed due to client error")    # noqa: E501
