# Jarvis - Voice Assistant

## Installation

To use the Jarvis voice assistant, you'll need to have the following dependencies installed:

- `speech_recognition`
- `pyttsx3`
- `requests`
- `pygame`
- `difflib`

You can install these dependencies using pip:

```
pip install speech_recognition pyttsx3 requests pygame
```

## Usage

To run the Jarvis voice assistant, simply execute the `chatbot.py` file:

```
python chatbot.py
```

Jarvis will start listening for your voice commands and respond accordingly. Some of the available commands include:

- "What time is it?"
- "What's the weather like?"
- "Play music"
- "Stop music"
- "Open Google"
- "Open YouTube"
- "Goodbye"

## API

The Jarvis voice assistant provides the following methods:

- `set_voice()`: Sets the voice properties for the text-to-speech engine.
- `speak(text)`: Converts the given text to speech and plays it.
- `listen()`: Listens for user voice input and returns the recognized text.
- `open_google()`: Opens the Google website in the default web browser.
- `open_youtube()`: Opens the YouTube website in the default web browser.
- `get_time()`: Returns the current time.
- `get_date()`: Returns the current date.
- `search_knowledge_base(query)`: Searches the knowledge base for an answer to the given query.
- `play_music(query=None)`: Plays a random song from the specified music directory, or a song matching the given query.
- `stop_music()`: Stops the currently playing music.
- `get_weather(city="Siliguri")`: Retrieves the current weather information for the specified city.
- `forecast_weather(city="Siliguri")`: Retrieves the 5-day weather forecast for the specified city.
- `process_command(command)`: Processes the given user command and determines the appropriate action.
- `run()`: Starts the main loop for the voice assistant.

## Contributing

If you'd like to contribute to the Jarvis voice assistant, feel free to submit a pull request. Please make sure to follow the existing code style and include appropriate tests for any new functionality.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To run the tests for the Jarvis voice assistant, you can use the following command:

```
python -m unittest discover tests
```

This will run all the test cases located in the `tests` directory.