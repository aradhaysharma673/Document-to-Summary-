from pydantic import BaseModel, Field, field_validator

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=100, max_length=50000)
    max_sentences: int = Field(default=5, ge=1, le=20)
    
    @field_validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    sentences_count: int
    truncated: bool

class HealthResponse(BaseModel):
    status: str
    version: str
    model_ready: bool
    requests_remaining: int
