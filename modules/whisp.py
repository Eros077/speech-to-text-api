import os
import openai

from modules.chatGPT import procesHistoria, getBrief, fillHdv
from modules.db import updateInterview
from modules.slice_audio import chop_audio
from modules.notification import notificacion

async def transcription(interview_id, audio_data, size, userId, mail):
    API_KEY = "your_openai_api_key"
    model_id = 'whisper-1'

    with open("../audio/{}.mp3".format(interview_id), "wb") as file: #creacion del archivo mp3; aca escribo los bytes en un archivo (Write Bytes, wb) y le agrego el .mp3
            file.write(audio_data)

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    path_to_audio = os.path.join(directorio_actual, '../audio/{}.mp3'.format(interview_id))

    if(size):
        chop_audio(path_to_audio, interview_id)

    trans_text = ""
    counter = 1

    for i in range(1, 5):
        chunk_path = os.path.join(directorio_actual, '../audio/{}_{}.mp3'.format(interview_id, counter))
        media_file = open(chunk_path, "rb")

        response = openai.Audio.transcribe(
            api_key = API_KEY,
            model = model_id,
            file = media_file,
            response_format = 'json'#text, json, srt, vtt
        )
        media_file.close()
        trans_text += response['text']
        counter += 1
        os.remove(chunk_path)

    texto_original = trans_text
    texto_procesado = procesHistoria(texto_original)
    brief = getBrief(texto_original)

    camposExtraidosHdv = fillHdv(texto_original)

    updateInterview(interview_id, "done", texto_original, texto_procesado, brief, camposExtraidosHdv)
    notificacion(mail , userId)
    print("Interview transcripta y guardada con id:{}".format(interview_id))


