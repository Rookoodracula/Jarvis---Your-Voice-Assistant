import speech_recognition as sr
import pyttsx3
import datetime
import requests
import os
import random
import time
import pygame
import webbrowser
import json
from difflib import get_close_matches


class VoiceAssistant:
    def __init__(self, name="Assistant"):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.set_voice()

        # Assistant name
        self.name = name

        # Music player setup
        pygame.mixer.init()
        self.current_song = None
        self.is_playing = False

        # Weather API setup - you'll need to get your own API key
        self.weather_api_key = "e4da04c8ed6e262935352917dbbb0f17"

        # Load knowledge base for Q&A
        self.knowledge_base = {
            "hello": "Hello! How can I help you today?",
            "what can you do": "I can tell you the time, play music, check the weather, answer questions, and more.",
            "how are you": "I'm functioning well, thank you for asking!",
            "goodbye": "Goodbye! Have a great day!",
            "who created you": "Abhirup Basu",
            "tell me a joke": "Why was the computer cold? It left its Windows open",
            "tell me another joke": "Why don’t programmers like nature? It has too many bugs",
            "tell me about yourself": "I act as a virtual assistant that can process voice commands and perform various tasks. \
            I uses speech recognition, text-to-speech, and NLP techniques to interact with you",
            "what is your name": "my name is Jarvis, your voice assistant"
        }

        # Command history
        self.command_history = []

        # Start message
        self.speak(f"{self.name} is ready. How can I help you?")

    def set_voice(self):
        """Set the voice properties"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Index 1 is usually a female voice
        self.engine.setProperty('rate', 180)  # Speed of speech

    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen for user voice input"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
                return ""
            except sr.RequestError:
                self.speak("I'm having trouble accessing the speech recognition service.")
                return ""

    def open_google(self):
        webbrowser.open("https://www.google.com")
        self.speak("Opening Google.")

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")
        self.speak("Opening YouTube.")

    def get_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_string = now.strftime("%I:%M %p")
        return f"The current time is {time_string}."

    def get_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        date_string = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_string}."

    def search_knowledge_base(self, query):
        """Search for answer in knowledge base"""
        # Find closest match to query
        matches = get_close_matches(query, self.knowledge_base.keys(), n=1, cutoff=0.6)
        if matches:
            return self.knowledge_base[matches[0]]
        else:
            return "I'm not sure how to answer that yet."

    def play_music(self, query=None):
        """Play music from a specified directory"""
        music_dir = "C:\\Users\\4ever\\PycharmProjects\\PythonProject\\music"  # Replace with your music directory path

        if not os.path.exists(music_dir):
            return "I couldn't find the music directory."

        songs = [os.path.join(music_dir, f) for f in os.listdir(music_dir)
                 if f.endswith(('.mp3', '.wav'))]

        if not songs:
            return "No music files found in the directory."

        # Stop currently playing music if any
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

        # If query is provided, try to find matching song
        if query:
            query = query.lower()
            matching_songs = [song for song in songs if query in os.path.basename(song).lower()]
            if matching_songs:
                songs = matching_songs
            else:
                return f"No songs matching '{query}' were found."

        # Play a random song from the filtered list
        self.current_song = random.choice(songs)
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play()
        self.is_playing = True

        song_name = os.path.basename(self.current_song)
        return f"Playing {song_name}"

    def stop_music(self):
        """Stop playing music"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            return "Music stopped."
        else:
            return "No music is currently playing."

    def get_weather(self, city="Siliguri"):
        """Get weather forecast for a city"""
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.weather_api_key,
                'units': 'metric'  # Use 'imperial' for Fahrenheit
            }

            response = requests.get(base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                weather_desc = data['weather'][0]['description']
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']

                forecast = (f"The weather in {city} is currently {weather_desc}. "
                            f"The temperature is {temp:.1f}°C, with humidity at {humidity}% "
                            f"and wind speed of {wind_speed} meters per second.")

                # Add weather prediction based on conditions
                if temp > 25:
                    forecast += " It's quite warm, so dress lightly."
                elif temp < 10:
                    forecast += " It's cold today, consider wearing a coat."

                if "rain" in weather_desc:
                    forecast += " Don't forget your umbrella!"

                return forecast
            else:
                return f"I couldn't get the weather for {city}. Please check the city name."

        except Exception as e:
            return f"Error retrieving weather information: {str(e)}"

    def forecast_weather(self, city="Siliguri"):
        """Get 5-day weather forecast for a city"""
        try:
            base_url = "http://api.openweathermap.org/data/2.5/forecast"
            params = {
                'q': city,
                'appid': self.weather_api_key,
                'units': 'metric'  # Use 'imperial' for Fahrenheit
            }

            response = requests.get(base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                forecast_text = f"5-day weather forecast for {city}:\n"

                # Group forecast data by day (the API returns data in 3-hour intervals)
                daily_forecasts = {}
                for item in data['list']:
                    date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')

                    if date not in daily_forecasts:
                        daily_forecasts[date] = {
                            'temps': [],
                            'descriptions': []
                        }

                    daily_forecasts[date]['temps'].append(item['main']['temp'])
                    daily_forecasts[date]['descriptions'].append(item['weather'][0]['description'])

                # Create a summary for each day
                for i, (date, forecast) in enumerate(list(daily_forecasts.items())[:5]):
                    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                    day_name = date_obj.strftime('%A')

                    avg_temp = sum(forecast['temps']) / len(forecast['temps'])

                    # Find most common weather description
                    from collections import Counter
                    desc_counter = Counter(forecast['descriptions'])
                    common_desc = desc_counter.most_common(1)[0][0]

                    if i == 0:
                        day_text = "Today"
                    elif i == 1:
                        day_text = "Tomorrow"
                    else:
                        day_text = day_name

                    forecast_text += f"{day_text}: {common_desc}, average temperature {avg_temp:.1f}°C\n"

                return forecast_text
            else:
                return f"I couldn't get the forecast for {city}. Please check the city name."

        except Exception as e:
            return f"Error retrieving forecast information: {str(e)}"

    def process_command(self, command):
        """Process user command and determine action"""
        if not command:
            return ""

        # Add to command history
        self.command_history.append(command)

        # Process commands
        if "time" in command:
            return self.get_time()

        elif "date" in command or "day" in command:
            return self.get_date()

        elif "play music" in command or "play song" in command:
            song_query = None
            if "play" in command and "music" not in command and "song" not in command:
                # Extract song name after "play"
                song_query = command.split("play ", 1)[1]
            return self.play_music(song_query)

        elif "stop music" in command or "pause music" in command:
            return self.stop_music()

        elif "weather" in command and "forecast" in command:
            # Extract city name if provided
            city = "Siliguri"  # Default city
            if "in" in command:
                city_part = command.split("in", 1)[1].strip()
                if city_part:
                    city = city_part
            return self.forecast_weather(city)

        elif "weather" in command:
            # Extract city name if provided
            city = "Siliguri"  # Default city
            if "in" in command:
                city_part = command.split("in", 1)[1].strip()
                if city_part:
                    city = city_part
            return self.get_weather(city)

        elif "exit" in command or "quit" in command or "goodbye" in command:
            self.speak("Goodbye!")
            return "exit"

        elif "open google" in command:
            self.open_google()
        elif "open youtube" in command:
            self.open_youtube()

        else:
            return self.search_knowledge_base(command)

    def run(self):
        """Main loop for the voice assistant"""
        running = True

        while running:
            command = self.listen()
            response = self.process_command(command)

            if response == "exit":
                running = False
            elif response:
                self.speak(response)


if __name__ == "__main__":
    assistant = VoiceAssistant("Jarvis")  # You can change the name to whatever you like
    assistant.run()