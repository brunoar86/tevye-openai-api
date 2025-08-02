import aiohttp
import tiktoken

from tevye_openai_api.app.settings.openai import project


class ChatCompletion:

    def __init__(self):
        self.OPENAI_API_KEY = project.key()
        self.PROJECT_ID = project.id()
        self.ORGANIZATION_ID = project.organization()
        self.input = None

    def assemble_request(self):
        url = 'https://api.openai.com/v1/chat/completions'

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

    def assemble_response_data(self, response):
        model = None
        messages = []
        logprobs = None

        messages.append(response['choices'][0]['message'])
        model = response['model']
        if 'logprobs' in response['choices'][0]:
            logprobs = response['choices'][0]['logprobs']

        data = {
            'model': model,
            'messages': messages,
            'logprobs': logprobs
        }

        return data

    def collect_usage_data(self, response):
        print('INFO:     Request object: {}'.format(response['object']))
        print('INFO:     Request usage: {} tokens.'
              .format(response['usage']['total_tokens']))

    async def request(self, input):

        self.input = input

        req = self.assemble_request()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=req['url'], headers=req['headers'],
                                        json=req['payload']) as response:
                    if response.status == 200:
                        response = await response.json()
                        data = self.assemble_response_data(response)
                        self.collect_usage_data(response)
                        return data
                    else:
                        response = await response.json()
                        print('ERROR:   {}'.format(response['error']['message']))    # noqa: E501
            except aiohttp.ClientError as error:
                print('Erro: {}'.format(error))

    def map_logit_bias(self, logit_bias: dict, model: str):
        if logit_bias is None:
            pass
        else:
            logit_bias = dict()
            encoder = tiktoken.encoding_for_model(model)
            for k, v in logit_bias.items():
                tokens = encoder.encode(k)
                if len(tokens) > 1:
                    for token in tokens:
                        logit_bias[str(token)] = v
                else:
                    logit_bias[str(tokens[0])] = v

        return logit_bias
