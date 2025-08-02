from typing import Optional
from pydantic import BaseModel


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[object] = None
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[dict] = None
    logprobs: Optional[bool] = False
    max_completion_tokens: Optional[int] = 100
    modalities: Optional[list] = ['text']
    n: Optional[int] = 1
    parallel_tool_calls: Optional[bool] = None
    prediction: Optional[dict] = None
    presence_penalty: Optional[float] = 0.0
    reasoning_effort: Optional[dict] = None
    response_format: Optional[dict] = None
    stream: Optional[bool] = False
    temperature: Optional[float] = 1.0
    tool_choice: Optional[str | dict] = None
    tools: Optional[list] = None
    top_logprobs: Optional[int] = None
    top_p: Optional[float] = 1.0
    web_search_options: Optional[dict] = None
