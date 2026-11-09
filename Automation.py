import subprocess
import webbrowser
import requests
import asyncio
import keyboard
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")


client = Groq(api_key=GroqAPIKey)


SystemChatBot = [
    {"role": "system", "content": "Hello, you are a content writer. You must generate high-quality content."}
]

# Functions for opening and closing apps on macOS
def open_app(app_name):
    """Opens an application on macOS."""
    try:
        subprocess.run(["open", "-a", app_name])
        return True
    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        return False

def close_app(app_name):
    """Closes an application on macOS."""
    try:
        subprocess.run(["pkill", "-f", app_name])
        return True
    except Exception as e:
        print(f"Error closing {app_name}: {e}")
        return False

# Google Search function
def google_search(query):
    search(query)
    return True

# YouTube Search function
def youtube_search(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    return True

# Play a YouTube video
def play_youtube(query):
    playonyt(query)
    return True

# AI Content Generation
def content_writer(prompt):
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        messages=SystemChatBot + messages,
        model="mixtral-8x7b-32768",
        max_tokens=2048,
        temperature=0.7
    )
    response = completion.choices[0].message["content"]
    messages.append({"role": "assistant", "content": response})
    return response

def generate_content(topic):
    topic = topic.replace("content", "").strip()
    content = content_writer(topic)
    
    file_name = f"Data/{topic.lower().replace(' ', '_')}.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Content saved in {file_name}")
    return True

# System control functions (Volume, Mute, etc.)
def system_control(command):
    key_mapping = {
        "mute": "volume mute",
        "unmute": "volume mute",
        "volume up": "volume up",
        "volume down": "volume down"
    }
    
    if command in key_mapping:
        keyboard.press_and_release(key_mapping[command])
        return True
    return False


async def execute_commands(commands):
    tasks = []
    
    for command in commands:
        if command.startswith("open"):
            app_name = command.replace("open", "").strip()
            tasks.append(asyncio.to_thread(open_app, app_name))
        elif command.startswith("close"):
            app_name = command.replace("close", "").strip()
            tasks.append(asyncio.to_thread(close_app, app_name))
        elif command.startswith("play"):
            video_name = command.replace("play", "").strip()
            tasks.append(asyncio.to_thread(play_youtube, video_name))
        elif command.startswith("content"):
            topic = command.replace("content", "").strip()
            tasks.append(asyncio.to_thread(generate_content, topic))
        elif command.startswith("google search"):
            query = command.replace("google search", "").strip()
            tasks.append(asyncio.to_thread(google_search, query))
        elif command.startswith("youtube search"):
            query = command.replace("youtube search", "").strip()
            tasks.append(asyncio.to_thread(youtube_search, query))
        elif command.startswith("system"):
            system_command = command.replace("system", "").strip()
            tasks.append(asyncio.to_thread(system_control, system_command))
        else:
            print(f"No function found for command: {command}")

    results = await asyncio.gather(*tasks)
    return results

if __name__ == '__main__':
    while True:
        user_command = input("Enter commands (comma-separated) or type 'exit' to quit: ").strip().lower()

        if user_command == "exit":
            print("Exiting...")
            break  # Stop the loop

        # Split multiple commands by comma and execute them together
        command_list = [cmd.strip() for cmd in user_command.split(",")]

        asyncio.run(execute_commands(command_list))


