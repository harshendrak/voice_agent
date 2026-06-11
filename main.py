
import speech_recognition as sr
from kokoro import KPipeline
import sounddevice as sd
from openai import OpenAI
from dotenv import load_dotenv
import re

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

            SYSTEM_PROMPT =  f"""
            You are a voice assistant.

            Think silently.
            Never reveal your reasoning.
            Never reveal intermediate thoughts.
            Never output thinking process.
            Never output <thought> tags.
            Only output the final answer.

            Respond naturally for spoken conversation.
            Keep responses concise.
            Avoid markdown.
            Avoid lists.
            Avoid special formatting.
"""

          

            stt = r.recognize_google(audio) #type: ignore

            print("You: ",stt)
            client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
            response = client.chat.completions.create(
        model="gemma-4-31b-it",
        messages=[
            {   "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": stt
            }
        ]
    )

        tts = response.choices[0].message.content or ""

        tts = re.sub(
        r"<thought>.*?</thought>",
        "",
        tts,
        flags=re.DOTALL
        ).strip()

        print("Assistant:", tts)

        speak(tts)
            

if __name__ == "__main__":
    main()
