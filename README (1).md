# NexAI

NexAI is a Python-based AI voice assistant with a desktop GUI. Speak to it, and it decides what to do: chat, search the web in real time, open apps, play videos, or generate images. It answers out loud.

## Features

- **Voice input**: speech-to-text through the browser's speech recognition (Selenium + Chrome)
- **Voice output**: natural-sounding text-to-speech with Microsoft Edge TTS
- **Chatbot**: conversational AI powered by Groq, with saved chat history
- **Real-time search**: Google search results fed to the AI for up-to-date answers
- **Decision layer**: a Cohere model classifies each request (chat, search, automation, image, exit)
- **Automation**: open and close apps, play YouTube videos, Google and YouTube search, system commands
- **Image generation**: Stable Diffusion XL through the Hugging Face Inference API
- **Desktop GUI**: PyQt5 interface with a microphone toggle, chat view and status display

## Project Structure

```
NexAi/
├── Main.py                  # Entry point: ties the GUI and backend together
├── Requirements.txt         # Python dependencies
├── Backend/
│   ├── Model.py             # Decision-making layer (Cohere)
│   ├── Chatbot.py           # General conversation (Groq)
│   ├── RealtimeSearchEngine.py
│   ├── Automation.py        # Open/close apps, play, search, system
│   ├── ImageGeneration.py   # Image generation (Hugging Face)
│   ├── SpeechToText.py
│   └── TextToSpeech.py
├── Frontend/
│   ├── GUI.PY               # PyQt5 interface
│   ├── Graphics/            # Icons and images
│   └── Files/               # Temporary status/response data files
└── Data/
    ├── ChatLog.json         # Chat history
    └── Voice.html           # Speech recognition page
```

## Requirements

- Windows (the project uses Windows-style file paths and app control)
- Python 3.10 or newer
- Google Chrome (used for speech recognition)
- A microphone
- API keys for:
  - [Groq](https://console.groq.com/)
  - [Cohere](https://dashboard.cohere.com/)
  - [Hugging Face](https://huggingface.co/settings/tokens)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/santhoshakkineni3-cell/NexAI.git
   cd NexAI
   ```

2. (Recommended) Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r Requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```env
   Username=YourName
   Assistantname=NexAI
   GroqAPIKey=your_groq_api_key
   CohereAPIkey=your_cohere_api_key
   HuggingFaceAPIKey=your_huggingface_api_key
   InputLanguage=en
   AssistantVoice=en-US-JennyNeural
   ```

   > Never commit your `.env` file. It is already listed in `.gitignore`.

## Usage

```bash
python Main.py
```

1. The GUI window opens.
2. Click the microphone icon to start listening.
3. Speak a command, for example:
   - "What's the capital of France?"
   - "What's the latest news on AI?"
   - "Open Notepad"
   - "Play Believer on YouTube"
   - "Generate image of a sunset over mountains"
4. NexAI replies on screen and out loud.

## Tech Stack

Python · PyQt5 · Groq · Cohere · Hugging Face · Selenium · Edge TTS · Pygame

## Contributing

Issues and pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

No license has been chosen yet. Add one (for example MIT) if you want others to be able to reuse this code.
