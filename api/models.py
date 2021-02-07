from typing import Optional
from pydantic import BaseModel, Field
import uuid

class StudentModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    roll_no: int
    fees_paid: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "id": "0010203-0405-0607-0809-0a0badsa0d0e0f",
                "name": "John Doe",
                "roll_no": 23,
                "fees_paid": True
            }
        }