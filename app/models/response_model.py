from pydantic import BaseModel
from typing import List

class ReviewResponse(BaseModel):
    found_files: List[str]
    downsides: List[str]
    rating: str
    conclusion: str
