import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice") 

async def TextToAudioFile(text) -> None:
    file_path = os.path.join("Data", "speech.mp3")
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

def TTS(Text, func=lambda r=None: True):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(TextToAudioFile(Text))

        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("Data", "speech.mp3"))
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            if not func():
                break
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error in TTS: {e}")
    
    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information."
    ]
    
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Data[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

if __name__ == "__main__":
    try:
        while True:
            text = input("Enter the text (or type 'exit' to quit): ")
            if text.lower() == "exit":
                break
            TextToSpeech(text)
    except KeyboardInterrupt:
        print("\nExiting...")
