import streamlit as st
from deep_translator import GoogleTranslator
import random
import requests
import nltk
from nltk.corpus import wordnet
from gtts import gTTS
import io
import speech_recognition as sr
from io import BytesIO

# Download WordNet if not already available
nltk.download("wordnet")


# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Select a Section", ["Language Translator", "English Learning Word Quiz", "Audio File Transcription"])

# Language Translator
if section == "Language Translator":
    st.title(":earth_africa: Language Translator")

    text = st.text_input("Enter text to translate:")
    source_lang = st.selectbox("From", ["auto", "pt", "en", "es", "fr", "de", "zh"])
    target_lang = st.selectbox("To", ["pt", "en", "es", "fr", "de", "zh"])

    if st.button("Translate"):
        try:
            translation = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
            st.markdown(f"**Translation:** {translation}")
        except Exception as e:
            st.error(f"Translation failed: {e}")

# English Learning Word Quiz
elif section == "English Learning Word Quiz":
    st.title(":abc: English Learning Word Quiz")

    if "word" not in st.session_state:
        st.session_state.word = None

    # Get a random word dynamically from an API
    def get_random_word():
        try:
            response = requests.get("https://random-word-api.herokuapp.com/word")
            if response.status_code == 200:
                return response.json()[0]
        except:
            return "hello"  # Fallback word if API fails


    def get_word_details(word):
        """Fetches part of speech, definition, and an example sentence using NLTK's WordNet."""
        try:
            synsets = wordnet.synsets(word)

            if synsets:
                definition = synsets[0].definition()  # Definition
                example = synsets[0].examples()[0] if synsets[0].examples() else "No example available."
                return definition, example
            else:
                return "No definition found.", "No example found."
        except Exception as e:
            # If there is any error, return fallback messages
            return "An error occurred while fetching word details.", "No example found."

    def text_to_speech(text, lang):
        """Convert text to speech and return an in-memory audio file."""
        try:
            tts = gTTS(text=text, lang=lang)
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            return audio_bytes
        except Exception as e:
            st.error(f"TTS failed: {e}")
            return None

    source_lang_quiz = "en"  # Fixed to English
    target_lang_quiz = st.selectbox("To", ["es", "fr", "de", "pt"])

    # Button to generate a new word
    if st.button("New Word") or st.session_state.word is None:
        st.session_state.word = get_random_word()

    # Get the stored word
    word = st.session_state.word
    definition, example = get_word_details(word)

    # Translate it dynamically
    translator = GoogleTranslator(source=source_lang_quiz, target=target_lang_quiz)
    correct_translation = translator.translate(word)

    st.subheader(f"Translate this word: **{word}**")
    st.write(f":book: **Definition:** {definition}")
    st.write(f":books: **Example Sentence:** {example}")
    if st.button(":sound: Hear Original Word"):
        audio_data = text_to_speech(word, source_lang_quiz)
        if audio_data:
            st.audio(audio_data, format="audio/mp3")

    user_input = st.text_input("Your answer:")

    # Store previous results in session state
    if "quiz_history" not in st.session_state:
        st.session_state.quiz_history = []

    if st.button("Check Answer"):
        if user_input.lower().strip() == correct_translation.lower().strip():
            st.success(f":white_check_mark: Correct! The translation of '{word}' is **{correct_translation}**.")
            st.session_state.quiz_history.append(f":white_check_mark: {word} → {correct_translation}")
        else:
            st.warning(f":x: Incorrect! The correct translation is **{correct_translation}**.")
            st.session_state.quiz_history.append(f":x: {word} → {correct_translation} (Your answer: {user_input})")

    # Show translation history
    st.subheader("📝 Your Quiz History")
    for item in st.session_state.quiz_history[-5:]:  # Show last 5 attempts
        st.write(item)

# Audio File Transcription
elif section == "Audio File Transcription":
    st.title(" :speech_balloon: Audio File Transcription")

    # File uploader to upload an audio file (wav, aiff, flac)
    audio_file = st.file_uploader("Upload an Audio File (wav, aiff, flac)", type=["wav", "aiff", "flac"])

    # If an audio file is uploaded, process it
    if audio_file is not None:
        # Display the uploaded file name
        st.write(f"File uploaded: {audio_file.name}")

        # Convert the audio file to a format that can be processed
        audio_bytes = audio_file.read()
        audio_file = BytesIO(audio_bytes)

        # Initialize recognizer
        recognizer = sr.Recognizer()

        try:
            # Recognize the speech from the audio file
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)  # Record the entire audio file

            # Use Google's speech recognition to convert audio to text
            transcript = recognizer.recognize_google(audio_data)

            # Display the transcript
            st.subheader("Transcript")
            st.write(transcript)

        except Exception as e:
            st.error(f"Sorry, we couldn't process the audio file. Error: {e}")
