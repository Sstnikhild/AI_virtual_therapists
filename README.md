# Emotion Detection and Text-to-Speech (TTS) Application

This FastAPI-based application provides the functionality to detect emotions from both text and voice input and generate text-to-speech (TTS) audio based on a conversation. The application utilizes the OpenAI API for natural language processing and Eleven Labs API for generating TTS audio. Additionally, the project integrates emotion detection from voice using the `librosa` library.

## Features
- **Text Emotion Detection:** Detects emotions (e.g., sadness, anger, joy, anxiety) from a provided text.
- **Voice Emotion Detection:** Detects emotions from an audio file (.wav, .mp3, .ogg) based on pitch, intensity, and tempo.
- **Chat & Text-to-Speech:** Takes a message as input, processes it through OpenAI's GPT-3.5, and generates a spoken response using Eleven Labs' TTS API.
  
## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- OpenAI API Key
- Eleven Labs API Key
- librosa
- requests
- transformers
- .env file for storing API keys

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/emotion-detection-tts.git
cd emotion-detection-tts
```

### 2. Install Dependencies

Make sure you have Python 3.8+ installed and then install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Create `.env` File

In the project root directory, create a `.env` file and add your OpenAI API key, Eleven Labs API key, and other required variables.

```env
OPENAI_API_KEY=your_openai_api_key
ELEVEN_LABS_API_KEY=your_eleven_labs_api_key
VOICE_ID=your_voice_id
```

### 4. Run the FastAPI Application

Run the FastAPI app with Uvicorn:

```bash
uvicorn main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### 1. **Detect Emotion from Text**
- **Endpoint:** `/emotion/text`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "text": "I am feeling great today!"
    }
    ```
- **Response:**
    ```json
    {
        "text": "I am feeling great today!",
        "emotion": "joy",
        "confidence": 0.95
    }
    ```

### 2. **Detect Emotion from Voice**
- **Endpoint:** `/emotion/voice`
- **Method:** `POST`
- **Request Body:** Upload an audio file (.wav, .mp3, .ogg).
- **Response:**
    ```json
    {
        "filename": "audio_file.mp3",
        "emotion": "anger",
        "features": {
            "pitch": 220.5,
            "intensity": 0.07,
            "tempo": 120.3
        }
    }
    ```

### 3. **Chat and Text-to-Speech**
- **Endpoint:** `/chat_tts`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "message": "Hello, how are you?"
    }
    ```
- **Response:**
    ```json
    {
        "message": "Operation successful",
        "chat_response": "I'm doing great, thank you for asking!",
        "audio_file": "generated_audio/response_audio.mp3"
    }
    ```

## How It Works

### Text Emotion Detection
This feature uses the `bhadresh-savani/distilbert-base-uncased-emotion` model from Hugging Face's `transformers` library. The model classifies the emotion of a given text into one of the predefined categories, including sadness, anger, joy, and anxiety.

### Voice Emotion Detection
For voice emotion detection, the application uses the `librosa` library to analyze the audio features such as pitch, intensity, and tempo. Based on these features, the application classifies the emotion as sadness, anger, joy, or anxiety.

### Chat & Text-to-Speech (TTS)
The system processes the user's text input through OpenAI's GPT-3.5 to generate a conversational response. The response is then converted into speech using the Eleven Labs Text-to-Speech API. The audio file is saved and returned in the response.

## Error Handling

The application handles errors related to invalid inputs, API failures, or unexpected issues. Appropriate HTTP exceptions are raised with helpful error messages to assist users.

## Contributing

Feel free to fork this repository, submit issues, and create pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```


- **Model Updates:** You can replace the emotion classification model with another pre-trained model if needed.
- **Additional APIs:** Add more features by integrating other APIs for advanced text analysis or TTS providers.
- **UI Integration:** Build a front-end for interacting with the API using tools like React or Vue.js, allowing users to upload files and send messages seamlessly.

Let me know if you need further assistance!
