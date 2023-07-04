from fastapi import FastAPI, BackgroundTasks
from modules.whisp import transcription
from modules.db import elderlyExists, createInterview

from pydantic import BaseModel, constr, HttpUrl
import httpx

app = FastAPI()

# validating the data:
class Audio_data(BaseModel):
    elderly_id: constr(regex=r'^[a-zA-Z0-9]{20}$')
    audio_url: HttpUrl
    email: str

@app.post("/story") #recivo el id del usuario por la url
async def root(audio_data:Audio_data, background_tasks: BackgroundTasks):
    elderly_id = audio_data.elderly_id
    audio_url = audio_data.audio_url
    email = audio_data.email
    size = False

    if (not elderlyExists(elderly_id)):
        print("ERROR: Elderly doesn't exist: {}".format(elderly_id))
        return {"message": "Elderly doesn't exist"}
    
    interview_id = createInterview(elderly_id, audio_url)

    # get audio request:
    async with httpx.AsyncClient() as client:
        response = await client.get(audio_url)
        if(response.status_code == 200):
            audio = response.content

            file_size = len(audio) # obtener el tamaño en bytes
            size_mb = file_size / (1024 * 1024) # pasarlos a mb
            if(size_mb>25):
                size = True

            background_tasks.add_task(transcription, interview_id, audio, size, elderly_id, email) #transcipcion
        else:
            print("no se pudo procesar el audio")
            return {"message": "no se pudo procesar el audio"}
    
    return {"message": "audio recibed, processing"}
