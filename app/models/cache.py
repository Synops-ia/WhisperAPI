import json

from pydantic import BaseModel


class TranscriptModel(BaseModel):
    fileName: str
    data: str

    def __str__(self):
        return json.dumps({
            "fileName": self.fileName,
            "data": self.data
        })
