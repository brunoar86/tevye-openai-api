import aiohttp
import json
import structlog

from fastapi.exceptions import HTTPException

from tevye_openai_api.app.settings.openai import project

log = structlog.get_logger(__name__='speech_to_text module')


class SpeechToText:

    def __init__(self):
        self.OPENAI_API_KEY = project.key()
        self.PROJECT_ID = project.id()
        self.ORGANIZATION_ID = project.organization()
        self.input = None
        self.mp3_path = 'tevye_openai_api/app/modules/stt/mp3/'

    def assemble_request(self):
        log.debug("Assembling STT request", input=dict(self.input))
        url = 'https://api.openai.com/v1/audio/transcriptions'

        headers = {
            'Authorization': 'Bearer {}'.format(self.OPENAI_API_KEY),
            'OpenAI-Project': self.PROJECT_ID,
            'OpenAI-Organization': self.ORGANIZATION_ID
        }

        form = aiohttp.FormData()

        for k, v in dict(self.input).items():
            if k == 'file_name':
                file_path = self.mp3_path + v + '.mp3'
                form.add_field('file', open(file_path, 'rb'),
                               filename=v + '.mp3', content_type='audio/mpeg')
            elif v is not None and not isinstance(v, str):
                form.add_field(str(k), json.dumps(v))
            elif v is not None:
                form.add_field(str(k), v)

        req = {
            'url': url,
            'headers': headers,
            'payload': form
        }

        log.debug("Assembled STT request", req=req['payload'])
        return req

    async def request(self, input):

        self.input = input

        req = self.assemble_request()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=req['url'], headers=req['headers'],
                                        data=req['payload']) as response:
                    log.debug("STT request sent", status=response.status)
                    if response.status == 200:
                        response = await response.json()
                        log.debug("STT response received", response=response)
                        return response
                    else:
                        status_code = response.status
                        response = await response.json()
                        log.error("STT request failed",
                                  status_code=status_code,
                                  response=response['error'])
                        raise HTTPException(status_code=status_code,
                                            detail=response['error']['message']
                                            )

            except aiohttp.ClientError as error:
                log.error("STT request failed due to client error",
                          error=str(error))
                raise HTTPException(status_code=500,
                                    detail="STT request failed due to client error")    # noqa: E501
