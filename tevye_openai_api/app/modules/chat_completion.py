import aiohttp
import tiktoken

from tevye_openai_api.app.settings.openai import project


class ChatCompletion:

    def __init__(self):
        self.OPENAI_API_KEY = project.key()
        self.PROJECT_ID = project.id()
        self.ORGANIZATION_ID = project.organization()
        self.model = None
        self.messages = None
        self.audio = None
        self.frequency_penalty = 0.0
        self.logit_bias = None
        self.logprobs = False
        self.max_completion_tokens = 100
        self.modalities = None
        self.n = 1
        self.parallel_tool_calls = None
        self.prediction = None
        self.presence_penalty = 0
        self.reasoning_effort = None

    def assemble_request(self):
        url = 'https://api.openai.com/v1/chat/completions'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.OPENAI_API_KEY),
            'OpenAI-Project': self.PROJECT_ID,
            'OpenAI-Organization': self.ORGANIZATION_ID
        }

        payload = {
            'model': self.model,
            'messages': self.messages,
            'frequency_penalty': self.frequency_penalty,
            'logit_bias': self.logit_bias,
            'logprobs': self.logprobs,
            'modalities': self.modalities,
            'n': self.n,
            'presence_penalty': self.presence_penalty
        }

        if self.parallel_tool_calls is not None:
            payload['parallel_tool_calls'] = self.parallel_tool_calls

        if self.prediction is not None:
            payload['prediction'] = self.prediction

        if self.reasoning_effort is not None:
            payload['reasoning_effort'] = self.reasoning_effort

        req = {
            'url': url,
            'headers': headers,
            'payload': payload
        }

        return req

    def assemble_response_data(self, response):
        self.messages.append(response['choices'][0]['message'])
        self.model = self.set_model(response['model'])
        if self.logprobs is True:
            self.logprobs = response['choices'][0]['logprobs']
        data = {
            'model': self.model,
            'messages': self.messages,
            'logprobs': self.logprobs
        }

        return data

    def collect_usage_data(self, response):
        print('INFO:     Request object: {}'.format(response['object']))
        print('INFO:     Request usage: {} tokens.'
              .format(response['usage']['total_tokens']))

    async def request(self, input):

        self.set_model(input.model)
        self.set_messages(input.messages)
        self.set_frequency_penalty(input.frequency_penalty)
        self.set_logit_bias(input.logit_bias, input.model)
        self.set_logprobs(input.logprobs)
        self.set_max_completion_tokens(input.max_completion_tokens)
        self.set_modalities(input.modalities)
        self.set_n(input.n)
        if input.parallel_tool_calls is not None:
            self.set_parallel_tool_calls(input.parallel_tool_calls)
        self.set_presence_penalty(input.presence_penalty)
        if input.prediction is not None:
            self.set_prediction(input.prediction)
        if input.reasoning_effort is not None:
            self.set_reasoning_effort(input.reasoning_effort)

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
                        print(await response.text)
            except aiohttp.ClientError as error:
                print('Erro: {}'.format(error))

    def set_model(self, model: str):
        self.model = model

    def set_messages(self, messages: list):
        self.messages = messages

    def set_frequency_penalty(self, frequency_penalty: float):
        self.frequency_penalty = frequency_penalty

    def set_logit_bias(self, logit_bias: dict, model: str):
        if logit_bias is None:
            pass
        else:
            self.logit_bias = dict()
            encoder = tiktoken.encoding_for_model(model)
            for k, v in logit_bias.items():
                tokens = encoder.encode(k)
                if len(tokens) > 1:
                    for token in tokens:
                        self.logit_bias[str(token)] = v
                else:
                    self.logit_bias[str(tokens[0])] = v

    def set_logprobs(self, logprobs: bool):
        self.logprobs = logprobs

    def set_max_completion_tokens(self, max_completion_tokens):
        self.max_completion_tokens = max_completion_tokens

    def set_modalities(self, modalities):
        self.modalities = modalities

    def set_n(self, n):
        self.n = n

    def set_parallel_tool_calls(self, parallel_tool_calls):
        self.parallel_tool_calls = parallel_tool_calls

    def set_prediction(self, prediction):
        self.prediction = prediction

    def set_presence_penalty(self, presence_penalty):
        self.presence_penalty = presence_penalty

    def set_reasoning_effort(self, reasoning_effort):
        self.reasoning_effort = reasoning_effort
