from pydantic import BaseModel, Field
from typing import Optional

class Note(BaseModel):
    id: Optional[str]
    title: Optional[str] = Field(default="")
    priority: int = Field(default=0)
    desc: Optional[str] = Field(default="")