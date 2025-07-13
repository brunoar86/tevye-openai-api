from typing import Optional
from pydantic import BaseModel


class TTSRequest(BaseModel):
    input: str = None
    model: str = None
    voice: str = None
    instructions: Optional[str] = None
    response_format: Optional[str] = None
    speed: Optional[float] = 1.0
    stream_format: Optional[str] = None
