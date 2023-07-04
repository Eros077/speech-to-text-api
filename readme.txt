This API was built for Amaia App, a mobile app to connect families with their grandparents.
The main purpose of this API is to collect life stories/information shared by the elderly. It helps 
psychologists reduce their workload, and families can access their 
loved ones' life stories whenever they want.

How does it work?
    - It receives a URL to download an audio file and a user ID.
    - It sends the audio to OpenAI's Whisper model, which returns a transcription from audio to text.
    - The transcription is then sent to ChatGPT to obtain detailed and specific information.
    - Finally, the data, including the original transcription and information from ChatGPT, is saved in Firestore.
    - An email notification is sent to announce the completion of the process.

Requirements:
    - Firebase project (refer to "firestore&storage.txt" for instructions)
    - OpenAI account (refer to "openAi.txt" for instructions)
    - Create a virtual environment in the project's folder.
    - Activate your virtual environment.
    - Install all the requirements listed in "requirements.txt" (if any package is missing from the .txt file, install it).

After completing these steps, ensure that the API is functioning correctly by running a local server:
    - Activate your virtual environment.
    - Execute the command: uvicorn main:app --reload.
    - Make a request to the server and wait; it may take some time.

Now you can deploy:
    - Create a Docker image.
    - Push the image to your cloud project.