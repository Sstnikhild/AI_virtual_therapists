async function startTherapySession() {
    const userInput = document.getElementById('userInput').value;

    if (userInput.trim() !== "") {
        document.getElementById('loading').style.display = 'block';

        try {
            const emotionResponse = await fetch("http://localhost:8000/emotion/text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: userInput }),
            });

            if (!emotionResponse.ok) throw new Error("Failed to detect emotion");

            const emotionData = await emotionResponse.json();
            const { emotion, confidence } = emotionData;

            document.getElementById("emotion-text").textContent = `${emotion} (Confidence: ${(confidence * 100).toFixed(2)}%)`;

            const chatResponse = await fetch("http://localhost:8000/chat_tts", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userInput }),
            });

            if (!chatResponse.ok) throw new Error(await chatResponse.text());

            const chatData = await chatResponse.json();
            const reply = chatData.chat_response;

            document.getElementById("chat-text").textContent = reply;

            playAudioResponse(chatData.audio_file);

        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            // Clear the input field and hide the spinner only if there was a successful response
            document.getElementById('userInput').value = ""; 
            document.getElementById('loading').style.display = 'none';
        }
    } else {
        alert("Please enter your thoughts before starting the session.");
    }
}


// Function to play the AI's audio response
function playAudioResponse(audioFile) {
    // Create a new Audio object each time a new audio file is received
    const audioPlayer = new Audio(audioFile);

    // Clear any previously playing audio to avoid overlap
    const allAudioPlayers = document.querySelectorAll('audio');
    allAudioPlayers.forEach(player => {
        if (!player.paused) {
            player.pause();  // Pause the currently playing audio
            player.currentTime = 0;  // Reset the audio to the start
        }
    });

    // Play the new audio response
    audioPlayer.play();

    // Optional: Show a visual feedback for speaking (like a waveform or animation)
    showSpeechWaveform(audioPlayer);
}

function showSpeechWaveform(audioPlayer) {
    const waveformContainer = document.getElementById("waveform-container");

    // Clear existing content
    waveformContainer.innerHTML = '';

    // Add a 3D sphere animation
    waveformContainer.classList.add("pulsating-sphere");

    // Remove animation after the audio ends
    audioPlayer.onended = () => {
        waveformContainer.classList.remove("pulsating-sphere");
        waveformContainer.innerHTML = '';  // Clean up animation
    };
}


// Microphone input functionality
let isRecording = false;

document.getElementById('recordButton').addEventListener('click', function () {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
});

function startRecording() {
    document.getElementById('recordButton').classList.add('recording');
    isRecording = true;

    // Start recording with Web Speech API or similar approach
    // Add your recording logic here
}

function stopRecording() {
    document.getElementById('recordButton').classList.remove('recording');
    isRecording = false;

    // Stop recording logic here
}
