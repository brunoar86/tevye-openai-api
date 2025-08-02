import aiohttp
import json

from tevye_openai_api.app.settings.openai import project


class SpeechToText:

    def __init__(self):
        self.OPENAI_API_KEY = project.key()
        self.PROJECT_ID = project.id()
        self.ORGANIZATION_ID = project.organization()
        self.input = None
        self.mp3_path = 'tevye_openai_api/app/modules/stt/mp3/'

    def assemble_request(self):
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

        return req

    async def request(self, input):

        self.input = input

        req = self.assemble_request()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=req['url'], headers=req['headers'],
                                        data=req['payload']) as response:
                    if response.status == 200:
                        response = await response.json()
                        return response
                    else:
                        status_code = response.status
                        response = await response.json()
                        print('ERROR:    {}: {}'.format(status_code,
                                                        response['error']))
            except aiohttp.ClientError as error:
                print('ERROR:   {}'.format(error))
