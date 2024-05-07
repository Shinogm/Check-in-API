from pydantic import BaseModel

class Finger(BaseModel):
    fingerprint: str
    tmp: bytes