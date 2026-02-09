import cv2
import streamlit as st
import time

st.set_page_config(page_title="Blink Monitor", layout="centered")
st.title("👁️ Live Blink Counter (Webcam)")

run = st.checkbox("Start Camera")

FRAME = st.image([])
status = st.empty()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

blink_count = 0
eyes_prev = 2
start_time = time.time()

cap = cv2.VideoCapture(0)

if run:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        eyes_now = 0

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            eyes_now = len(eyes)

        if eyes_prev >= 1 and eyes_now == 0:
            blink_count += 1

        eyes_prev = eyes_now

        elapsed = time.time() - start_time
        blink_rate = int((blink_count / elapsed) * 60) if elapsed > 5 else 0

        FRAME.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        status.markdown(f"""
        ### 👁️ Blinks counted: **{blink_count}**
        ### ⏱️ Blink rate: **{blink_rate} / min**
        """)

        if not run:
            break

cap.release()
