import json
import os
from dotenv import load_dotenv
import requests


def generate_speech(text_to_speak='Hello earthlings', output_filename="ad_audio.mp3"):

    load_dotenv()
    api_key = os.environ.get('API_KEY')
    model_name = "gemini-2.0-flash-preview-tts-1" 
    
    # Note: As of late 2024, the publicly documented model is often 'tts-1'. 
    # If the model name above gives an error, try 'tts-1'.
    # model_name = "tts-1"

    # The API endpoint for Text-to-Speech
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:synthesizeSpeech?key={api_key}"
    # The data payload for the API request
    payload = {
        "input": {
            "text": text_to_speak
        },
        "voice": {
            # For a list of available voices, refer to the Gemini API documentation
            "name": "en-US-Standard-F", 
            "languageCode": "en-US"
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        }
    }

    # Set the headers for the request
    headers = {
        'Content-Type': 'application/json'
    }

    print("Sending text-to-speech request...")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        # The response content is the binary audio data
        audio_content = response.content

        # Save the audio content to a file
        with open(output_filename, 'wb') as audio_file:
            audio_file.write(audio_content)
        
        print(f"Successfully generated audio file: {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        # Optionally, print the response text for more details on the error
        if e.response is not None:
            print(f"Error details: {e.response}")


generate_speech()