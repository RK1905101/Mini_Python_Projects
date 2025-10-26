import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button

keyboard = KeyboardController()
mouse = MouseController()

detector = HandDetector(maxHands=1, detectionCon=0.7)

# Keep track of which key is currently held down
current_key = None

def press_key(key):
    """Press and hold a key if not already pressed"""
    global current_key
    if current_key != key:
        release_key()  # release previous key
        keyboard.press(key)
        current_key = key
        print(f"Holding {key}")

def release_key():
    """Release currently held key"""
    global current_key
    if current_key:
        keyboard.release(current_key)
        print(f"Released {current_key}")
        current_key = None

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        fingers = detector.fingersUp(hands[0])

        if fingers == [0, 1, 0, 0, 0]:      # Index only
            press_key('w')
        elif fingers == [0, 1, 1, 0, 0]:    # Index + Middle
            press_key('s')
        elif fingers == [1, 0, 0, 0, 0]:    # Thumb only
            press_key('a')
        elif fingers == [0, 1, 1, 1, 0]:    # Index + Middle + Ring
            press_key('d')
        elif fingers == [0, 0, 0, 0, 0]:    # Fist
            release_key()
            mouse.press(Button.left); mouse.release(Button.left)
            print("Click")
        elif fingers == [1, 1, 1, 1, 1]:    # Open palm → exit
            print("Exit gesture detected! Closing program...")
            release_key()
            break
        else:
            release_key()
    else:
        release_key()

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit manually
        release_key()
        break

cap.release()
cv2.destroyAllWindows()
