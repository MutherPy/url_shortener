from pydantic import BaseModel, Field, AnyHttpUrl

class UrlInput(BaseModel):
    url: AnyHttpUrl = Field(..., max_length=2048, min_length=1)


class UrlOutput(BaseModel):
    short_code: str
    short_url: str