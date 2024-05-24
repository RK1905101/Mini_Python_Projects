#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
import mediapipe as mp
from pulsectl import Pulse

def main():
    pulse = Pulse('volume-control')

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=1, min_detection_confidence=0.75, min_tracking_confidence=0.75)
    draw = mp.solutions.drawing_utils

    capture = cv2.VideoCapture(0)

    try:
        while capture.isOpened():
            ret, frame = capture.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            volume_hand_landmarks = get_volume_hand_landmarks(frame, processed, draw, mpHands)

            if volume_hand_landmarks:
                distance = get_distance(frame, volume_hand_landmarks)
                vol = np.interp(distance, [50, 220], [0, 1])  # Scale volume to [0, 1]
                set_volume(pulse, vol)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()

def get_volume_hand_landmarks(frame, processed, draw, hands):
    volume_hand_landmarks = []

    if processed.multi_hand_landmarks:
        for handlm in processed.multi_hand_landmarks:
            for idx, found_landmark in enumerate(handlm.landmark):
                height, width , _ = frame.shape
                x, y = int(found_landmark.x * width), int(found_landmark.y * height)

                if idx == 4 or idx == 8:  # Assuming thumb and index finger are used for volume control
                    volume_hand_landmarks.append((x, y))
            draw.draw_landmarks(frame, handlm, hands.HAND_CONNECTIONS)

    return volume_hand_landmarks

def set_volume(pulse, volume):
    sinks = pulse.sink_list()
    for sink in sinks:
        pulse.volume_set_all_chans(sink, volume)

from math import hypot

def get_distance(frame, landmarks_list):
    if len(landmarks_list) < 2:
        return None

    (x1, y1), (x2, y2) = landmarks_list[0], landmarks_list[1]

    cv2.circle(frame, (x1, y1), 7, (0, 255, 0), cv2.FILLED)
    cv2.circle(frame, (x2, y2), 7, (0, 255, 0), cv2.FILLED)
    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    distance = hypot(x2 - x1, y2 - y1)
    return distance

if __name__ == '__main__':
    main()

