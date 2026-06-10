
import speech_recognition as sr
from kokoro import KPipeline
import sounddevice as sd
from openai import OpenAI
from dotenv import load_dotenv

import warnings

load_dotenv()
warnings.filterwarnings("ignore")

tts_pipeline = KPipeline(lang_code="a",repo_id="hexgrad/Kokoro-82M")

def speak(text):
    generator = tts_pipeline(
        text,
        voice="af_heart"
    )

    for _, _, audio in generator:
        sd.play(audio, 24000)
        sd.wait()
    

def main():
    while True:
        r = sr.Recognizer() #Speech to Text

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold=2
            print("Hey there - I'm listening...")
            speak("Hey there - I'm listening...")
            audio=r.listen(source)
            
            print("Processing audio (STT)")

            SYSTEM_PRMPT =  f"""
            You are a voice assistant.
            Respond naturally for spoken conversation.
            Do not use markdown.
            Do not use bullet points.
            Do not use numbered lists.
            Do not use paragraph breaks.
            Keep responses concise and easy to speak aloud.
"""


            stt = r.recognize_google(audio) #type: ignore

            print("You: ",stt)
            client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
            response = client.chat.completions.create(
        model="gemini-3.5-flash",
        messages=[
            {   "role": "system",
                "content": SYSTEM_PRMPT
            },
            {
                "role": "user",
                "content": stt
            }
        ]
    )

        tts = response.choices[0].message.content

        print("Assistant:", tts)

        speak(tts)
            

if __name__ == "__main__":
    main()
