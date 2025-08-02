from typing import Optional
from pydantic import BaseModel


class STTRequest(BaseModel):
    file_name: str = None
    model: str = 'whisper-1'
    chunking_strategy: Optional[str] | Optional[object] = None
    include: Optional[list] = None
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: Optional[str] = None
    stream: Optional[bool] = None
    temperature: Optional[float] = None
    timestamp_granularities: Optional[list] = None
