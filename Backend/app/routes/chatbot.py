from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv
import librosa
from transformers import pipeline
import requests

# Load environment variables from .env file 
load_dotenv()

# Initialize FastAPI router
router = APIRouter()

# API Keys
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICE_ID = os.getenv("VOICE_ID", "9BWtsMINqrJLrRacOk9x")

# Validate API keys
if not ELEVEN_LABS_API_KEY:
    raise RuntimeError("11 Labs API Key is missing. Please set it in your .env file.")
if not OPENAI_API_KEY:
    raise RuntimeError("OpenAI API Key is missing. Please set it in your .env file.")

# Initialize emotion classifier
text_emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")


class TextEmotionRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str


@router.post("/emotion/text")
async def detect_text_emotion(request: TextEmotionRequest):
    try:
        emotion_result = text_emotion_classifier(request.text)
        emotion_data = emotion_result[0]
        return {
            "text": request.text,
            "emotion": emotion_data["label"],
            "confidence": emotion_data["score"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting emotion from text: {str(e)}")

@router.post("/emotion/voice")
async def detect_voice_emotion(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith((".wav", ".mp3", ".ogg")):
            raise HTTPException(
                status_code=400,
                detail="Invalid audio file format. Please upload .wav, .mp3, or .ogg files.",
            )

        temp_dir = "temp_audio"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as audio_file:
            audio_file.write(await file.read())

        y, sr = librosa.load(file_path, sr=None)
        pitch = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())
        intensity = float(librosa.feature.rms(y=y).mean())
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        if pitch < 150 and intensity < 0.02:
            emotion = "sadness"
        elif pitch > 200 and intensity > 0.05:
            emotion = "anger"
        elif pitch > 150 and intensity < 0.03:
            emotion = "joy"
        else:
            emotion = "anxiety"

        os.remove(file_path)

        return {
            "filename": file.filename,
            "emotion": emotion,
            "features": {
                "pitch": pitch,
                "intensity": intensity,
                "tempo": tempo
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting emotion from voice: {str(e)}")

@router.post("/chat_tts")
async def chat_and_tts(request: ChatRequest):
    try:
        # Fetch response from OpenAI
        openai.api_key = OPENAI_API_KEY
        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.message},
            ]
        )
        response_text = chat_response['choices'][0]['message']['content'].strip()

        # Convert response text to speech using Eleven Labs
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key": ELEVEN_LABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": response_text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }
        response = requests.post(url, json=data, headers=headers, stream=True)

        if response.status_code != 200:
            raise Exception(f"Failed to generate TTS: {response.text}")

        # Save TTS audio
        output_dir = "generated_audio"
        os.makedirs(output_dir, exist_ok=True)
        filename = "response_audio.mp3"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Return chat response and audio file path
        return {
            "message": "Operation successful",
            "chat_response": response_text,
            "audio_file": file_path
        }
    except openai.error.OpenAIError as oe:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(oe)}")
    except requests.RequestException as re:
        raise HTTPException(status_code=500, detail=f"TTS API Error: {str(re)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")