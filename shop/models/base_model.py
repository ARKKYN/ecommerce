

from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID

class BaseModel(SQLModel):
  id: UUID = Field(default_factory=uuid4, primary_key=True)

  def get_id(self):
    return self.id
