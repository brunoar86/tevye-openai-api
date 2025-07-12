from typing import Optional
from pydantic import BaseModel


class ChatCompletionRequest(BaseModel):
    model: str
    messages: Optional[list] = None
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[dict] = None
    logprobs: Optional[bool] = False
    max_completion_tokens: Optional[int] = 100
    modalities: Optional[str] = ['text']
    n: Optional[int] = 1
    parallel_tool_calls: Optional[bool] = None
    prediction: Optional[dict] = None
    presence_penalty: Optional[float] = 0.0
    reasoning_effort: Optional[dict] = None
