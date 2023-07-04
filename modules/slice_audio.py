from pydub import AudioSegment
import os

def chop_audio(path_to_audio, userId):
    #obtengo el audio:
    audio = AudioSegment.from_mp3(path_to_audio)

    duration = audio.duration_seconds #obtengo la duracion total del audio
    chunk_duration = duration/4 # divido los trozos:

    start_time = 0
    end_time = chunk_duration
    counter = 1
    
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    for i in range(1, 5):
        new_file_path = os.path.join(directorio_actual, '../audio/{}_{}.mp3'.format(userId, counter))
        chunk = audio[start_time * 1000:end_time * 1000]  # Convert to milliseconds
        chunk.export(new_file_path, format='mp3')  # Save each chunk as a separate file
        start_time = end_time
        end_time += chunk_duration
        counter += 1
    
    os.remove(path_to_audio)
    
        