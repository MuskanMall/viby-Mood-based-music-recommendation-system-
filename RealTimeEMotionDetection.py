import cv2
from deepface import DeepFace
import os


def emotion_detection(img_path):

    frame = cv2.imread(img_path)

    if frame is None:
        raise IOError("Cannot open the image at the path:" + img_path)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    selected_emotions = ['angry', 'happy', 'sad', 'surprise', 'neutral']

    # Draw rectangles around detected faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8)

    dominant_emotion = None

    for (x, y, w, h) in faces:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 6)

            # Extract the face region from the frame
            face_region = frame[y:y+h, x:x+w]

            # Perform emotion analysis using DeepFace on the face region
            results = DeepFace.analyze(face_region, actions=['emotion'])

            if isinstance(results, list) and len(results) > 0:
                result = results[0]  # Access the first result if it's a list
                emotion_result = result['emotion']  # Access the emotion part of the result
                dominant_emotion = result['dominant_emotion']  # Access the dominant emotion

                if dominant_emotion not in selected_emotions:
                    next_dominating_emotion = max(emotion_result, key=emotion_result.get)

                    if next_dominating_emotion in selected_emotions:
                        dominant_emotion = next_dominating_emotion

    return dominant_emotion


# print(emotion_detection())