import uvicorn
from fastapi import FastAPI, UploadFile, File
from transcription import recognition, divide, remove_file
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AudioFile(BaseModel):
    offset: int
    duration: int
    filename: str
    language: str


@app.get("/")
def index():
    return {"name": "Hello World"}


@app.post("/upload")
async def handle_upload(file: UploadFile = File(...)):
    uploaded_file = open("uploaded_file.mp3", "wb")
    uploaded_file.write(file.file.read())
    return "Upload Successfully"


@app.post("/divide")
async def handle_divide(divider: dict):
    return divide(divider["divider"], "uploaded_file.mp3")


@app.post("/process")
async def handle_process(file: AudioFile):
    res = recognition(file.offset, file.duration, "uploaded_file.mp3", file.language)
    return res


@app.post("/delete")
async def handle_delete():
    remove_file("uploaded_file.mp3")
    remove_file("audio.wav")

    return "Deleted successfully"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", reload=True)
