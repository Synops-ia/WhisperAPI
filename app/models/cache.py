import json

from pydantic import BaseModel


class TranscriptModel(BaseModel):
    fileName: str
    data: str
    in_process: str

    def __str__(self):
        return json.dumps({
            "fileName": self.fileName,
            "data": self.data,
            "in_process": self.in_process
        })
