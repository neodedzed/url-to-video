from pydantic import BaseModel

class ScrapeUrl(BaseModel):
    url: str