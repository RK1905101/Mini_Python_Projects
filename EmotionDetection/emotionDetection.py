# Before Running this code, ensure you have the required libraries installed:
# pip install tensorflow opencv-python numpy
# Run this on kernel base(python 3.11.5)
# Important:
# press 'q' to quit the webcam window


# step 1 : this might take 30-60 secs to load the model
#Loading the model
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

# Load the model without loading the optimizer state
model = load_model("_mini_XCEPTION.102-0.66.hdf5", compile=False)

# Recompile the model with the correct learning rate parameter
optimizer = Adam(learning_rate=0.0001)  # use 'learning_rate' instead of 'lr'
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

#--------
# Load OpenCV's pre-trained Haar Cascade classifier for face detection
import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#--------
# Emotion labels (assumes 7 emotions as per your dataset)
import numpy as np


emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# def preprocess_face(face):
#     # Resize the face image to the same size as the model's input (48x48) and convert to grayscale
#     face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
#     face_resized = cv2.resize(face_gray, (48, 48))

#     # Normalize pixel values to [0, 1]
#     face_resized = face_resized / 255.0

#     # Reshape to (1, 48, 48, 1) since the model expects 4D input
#     face_resized = np.reshape(face_resized, (1, 48, 48, 1))
    
#     return face_resized
# Function to preprocess face image for prediction
def preprocess_face(face):
    # Convert to grayscale and resize to (64x64) to match model input
    face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face_resized = cv2.resize(face_gray, (64, 64))  # Resize to 64x64
    
    # Normalize pixel values (0-255 to 0-1)
    face_resized = face_resized / 255.0
    
    # Reshape to match model input (1, 64, 64, 1)
    face_resized = np.reshape(face_resized, (1, 64, 64, 1))
    return face_resized


def predict_emotion(face_image):
    # Preprocess the face image
    processed_face = preprocess_face(face_image)

    # Get the model's predictions (output is a probability distribution)
    predictions = model.predict(processed_face)
    
    # Get the emotion label with the highest probability
    emotion_index = np.argmax(predictions)
    emotion_label = emotion_labels[emotion_index]
    
    return emotion_label
#--------

# Start video capture from the webcam
# Start video capture from webcam
import cv2
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
      print("Error: Failed to capture frame from camera.")
      break
    
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) for the detected face
        face = frame[y:y+h, x:x+w]
        
        # Predict the emotion for the face
        emotion = predict_emotion(face)
        
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
        
        # Display the predicted emotion label above the rectangle
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255, 255), 2)
    
    # Display the resulting frame
    cv2.imshow('Emotion Detection', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()


# if you are reading this : you are awesome :D