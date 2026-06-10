# Voice Assistant

An intelligent voice assistant that listens to user input, processes it with Google's Gemini AI model, and responds naturally through text-to-speech.

## Features

- 🎤 **Speech Recognition**: Converts user voice input to text using Google's Speech Recognition API
- 🤖 **AI Processing**: Sends user queries to Google Gemini 3.5 Flash model via OpenAI-compatible API
- 🔊 **Text-to-Speech**: Generates natural-sounding speech responses using Kokoro TTS model
- 🔁 **Continuous Conversation**: Runs in an infinite loop to handle multiple interactions
- 🎯 **Optimized for Voice**: System prompt ensures responses are concise and suitable for spoken conversation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     VOICE ASSISTANT PIPELINE                      │
└─────────────────────────────────────────────────────────────────┘

    🎤 USER INPUT
       │
       │ (Audio via Microphone)
       ▼
┌──────────────────────────────┐
│  SPEECH RECOGNITION (STT)    │
│  SpeechRecognition + Google  │
│  • Capture audio             │
│  • Adjust ambient noise       │
│  • Convert to text           │
└──────────────────────────────┘
       │
       │ (User text string)
       ▼
┌──────────────────────────────┐
│  AI LANGUAGE MODEL           │
│  Google Gemini 3.5 Flash     │
│  • System prompt applied     │
│  • Generate response         │
│  • Ensure voice-friendly     │
└──────────────────────────────┘
       │
       │ (AI response text)
       ▼
┌──────────────────────────────┐
│  TEXT-TO-SPEECH (TTS)        │
│  Kokoro 82M Model            │
│  • Language: English          │
│  • Voice: af_heart           │
│  • Sample rate: 24kHz        │
└──────────────────────────────┘
       │
       │ (Audio stream)
       ▼
    🔊 SPEAKER OUTPUT
       │
       └─► User Hears Response
```

### Data Flow
```
User Speech → STT → Plain Text → LLM → Response Text → TTS → Speaker Audio
```

## Workflow

1. **Initialization**
   - Load environment variables from `.env` file
   - Initialize Kokoro TTS pipeline with language code "a" (assumed English variant)
   - Use voice style "af_heart" for natural speech

2. **Main Loop**
   - Display listening notification
   - Speak "Hey there - I'm listening..." via TTS
   - Capture audio from microphone
   - Adjust for ambient noise to improve accuracy

3. **Speech-to-Text**
   - Convert captured audio to text using Google Speech Recognition
   - Print recognized text for debugging

4. **LLM Processing**
   - Send text to Google Gemini 3.5 Flash model
   - Include system prompt to ensure natural, conversational responses
   - Receive AI-generated response

5. **Text-to-Speech**
   - Convert response text to audio using Kokoro TTS
   - Play audio through speakers at 24kHz sample rate
   - Wait for audio to finish before next iteration

## Installation

### Prerequisites
- Python 3.8+
- Microphone access
- Speaker/audio output device
- Google API credentials (for Gemini API access)

### Setup

1. **Clone/Navigate to the project**
   ```bash
   cd voice_agent
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the `voice_agent` directory
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

Run the voice assistant:

```bash
python main.py
```

The assistant will start listening and respond to your voice inputs. Press `Ctrl+C` to exit.

## Configuration

### System Prompt
The assistant uses a system prompt to guide its responses:
```
You are a voice assistant.
Respond naturally for spoken conversation.
Do not use markdown.
Do not use bullet points.
Do not use numbered lists.
Do not use paragraph breaks.
Keep responses concise and easy to speak aloud.
```

Modify this prompt in `main.py` (lines 37-43) to change the assistant's behavior.

### TTS Voice Settings
- **Language Code**: `"a"` (currently set in line 11)
- **Voice Style**: `"af_heart"` (currently set in line 18)
- **Sample Rate**: `24000` Hz (line 72)

## API Requirements

- **Google Gemini API**: Access via OpenAI-compatible endpoint
  - Base URL: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - Model: `gemini-3.5-flash`
  - Requires API key in environment variable

## Dependencies

See [requirements.txt](requirements.txt) for all Python packages.

Key libraries:
- **SpeechRecognition**: Audio input capture and Google Speech Recognition
- **kokoro**: Text-to-speech generation
- **sounddevice**: Audio playback
- **openai**: API client for Gemini
- **python-dotenv**: Environment variable management

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Microphone not detected | Ensure microphone is connected and enabled in system settings |
| No sound output | Check speaker volume and audio device settings |
| Google Speech API errors | Ensure internet connection is stable |
| API key not found | Verify `.env` file exists and contains `GOOGLE_API_KEY` |
| Kokoro model download fails | Check internet connection; model will be downloaded on first run |

## Performance Notes

- First run downloads the Kokoro-82M model (~200MB)
- Speech recognition requires internet connection (uses Google's cloud API)
- Response time depends on network latency and model processing speed

## Future Enhancements

- [ ] Add conversation history/context management
- [ ] Support multiple languages
- [ ] Add voice wake word detection
- [ ] Implement local speech recognition option
- [ ] Add response caching for repeated queries
- [ ] Support for multiple voice profiles

## License

This project is provided as-is for educational and development purposes.
