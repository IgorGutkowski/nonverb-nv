import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [photo, setPhoto] = useState('');
  const [videoStream, setVideoStream] = useState(null);
  const [hasCamera, setHasCamera] = useState(true);

  useEffect(() => {
    // Make a request to your Flask backend
    axios.get('http://localhost:5000/')
      .then(response => setMessage(response.data.message))
      .catch(error => console.error('Error fetching data:', error));

    // Start video stream
    startVideo();
  }, []);

  const startVideo = () => {
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
      .then(stream => {
        setVideoStream(stream);
        const videoElement = document.getElementById('video');
        videoElement.srcObject = stream;
      })
      .catch(error => {
        console.error('Error accessing webcam:', error);
        setHasCamera(false);
      });
  };

  const takePhoto = () => {
    const videoElement = document.getElementById('video');
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.width;
    canvas.height = videoElement.height;

    const context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/png');
    setPhoto(dataUrl);

    // Send the captured photo to Flask backend
    sendPhotoToBackend(dataUrl);
  };

  const sendPhotoToBackend = async (photoData) => {
    try {
      const response = await axios.post('http://localhost:5000/classify_emotion', {
        photo: photoData,
      });
      // Display the classified emotion in an alert
      alert(`Emotion: ${response.data.emotion}`);
    } catch (error) {
      console.error('Error sending photo to backend:', error);
    }
  };

  return (
    <div className="App">
      <h1>Nonverb</h1>
      {hasCamera ? (
        <div>
          <video id="video" width="320" height="240" autoPlay></video>
          <div>
            <button onClick={takePhoto}>Take Photo</button>
          </div>
          {photo && (
            <div>
              <h2>Captured Photo:</h2>
              <img src={photo} alt="Captured" width="320" height="240" />
            </div>
          )}
        </div>
      ) : (
        <div>
          <p>No camera detected on this device.</p>
          <p>{message}</p>
        </div>
      )}
    </div>
  );
}

export default App;
