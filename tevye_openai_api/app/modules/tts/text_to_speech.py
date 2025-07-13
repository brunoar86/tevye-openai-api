import os
import aiohttp

from tevye_openai_api.app.settings.openai import project


class TextToSpeech:

    def __init__(self):
        self.OPENAI_API_KEY = project.key()
        self.PROJECT_ID = project.id()
        self.ORGANIZATION_ID = project.organization()
        self.input = None
        self.mp3_path = 'tevye_openai_api/app/modules/tts/mp3/speech.mp3'

    def assemble_request(self):
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

        return req

    async def request(self, input):

        self.input = input

        req = self.assemble_request()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=req['url'], headers=req['headers'],
                                        json=req['payload']) as response:
                    if response.status == 200:
                        content = await response.read()
                        os.makedirs(os.path.dirname(self.mp3_path),
                                    exist_ok=True)
                        with open(self.mp3_path, 'wb') as file:
                            file.write(content)
                        print('INFO:     Audio saved in: {}'
                              .format(self.mp3_path))

                        return self.mp3_path
                    else:
                        print('ERROR:    {}: {}'.format(response.status,
                                                        await response.text))
            except aiohttp.ClientError as error:
                print('ERROR:   {}'.format(error))
