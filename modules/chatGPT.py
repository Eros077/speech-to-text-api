import openai
# Load your API key from an environment variable or secret management service
openai.api_key = "your_API_key"

# list engines
engines = openai.Engine.list()

def procesHistoria(contentTxt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "A continuación te voy a mostrar el texto de una entrevista a una persona mayor para evaluar su personalidad y conocerla mas a fondo.\
             Extrae de la entrevista los puntos más importantes en forma de bullet points. Un bullet point por linea.\
             Genera tambien un breve texto sobre su personalidad, forma d epensar y de que experiencias provienen estos pensamientos."},
            {"role": "system", "content": contentTxt},
        ]
    )
    story = response.choices[0]['message']['content'].strip()
    return story

def getBrief (text):
    # TODO: A pesar de que se le dice que no incluya nada como "La entrevista ha tratado sobre", lo sigue haciendo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "A continuación te voy a mostrar el texto de una entrevista a una persona mayor para evaluar su personalidad y conocerla mas a fondo. Quiero que me digas en una frase el tema principal que se ha tratado. En la respuesta no incluyas al inicio de la respuesta nada como \"La entrevista ha tratado sobre\" ni similares, sólo quiero la respuesta, se breve."},
            {"role": "system", "content": text},
        ]
    )
    brief = response.choices[0]['message']['content'].strip()


    return brief

def askText(text, question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Dado el siguiente texto de una entrevista a una persona mayor te van a hacer una preguntas. Debes responder brevemente y en caso de no encontrar la respuesta, desponde con \"No respondido\""},
            {"role": "system", "content": text},
            {"role": "user", "content": question}
        ]
    )
    answer = response.choices[0]['message']['content'].strip()

    if answer.startswith("No respondido"):
        return None

    return answer

def fillHdv (text):
    return {
        "fullName": askText(text, "¿Cuál es el nombre completo del entrevistado?"),
        "birthdate": askText(text, "¿Cuál es la fecha de nacimiento o cumpleaños del entrevistado? Respondeme en formator dia/mes/año"),
        "livedIn": askText(text, "¿En qué sitios ha vivido el entrevistado durante toda su vida?"),
        "workplaces": askText(text, "¿Qué trabajos ha tenido el entrevistado durante toda su vida?"),
        "achivements": askText(text, "¿Qué logros ha conseguido el entrevistado durante toda su vida?"),
        "languages": askText(text, "¿Qué idiomas ha aprendido a hablar el entrevistado durante toda su vida?"),
    }
