from pydantic import BaseModel, Field

class SimJobRequest(BaseModel):
    input_text: str = Field(min_length=1, description="Full .simc input")

class SimJobResult(BaseModel):
    ok: bool
    data: dict | None = None
    error: str | None = None
