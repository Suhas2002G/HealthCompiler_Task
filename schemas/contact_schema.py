from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional

class ContactCreate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=10)
    email: Optional[EmailStr] = None


class ContactResponse(BaseModel):
    id: int
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]

    class Config:
        from_attributes = True
