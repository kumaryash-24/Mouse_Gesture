import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize the video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

x1 = y1 = x2 = y2 = 0

while True:
    ret, image = cap.read()
    if not ret or image is None:
        print("Error: Unable to read from the camera.")
        break

    # Get image dimensions
    image_height, image_width, _ = image.shape

    # Flip the image horizontally for a mirror view
    image = cv2.flip(image, 1)

    # Convert the image to RGB for MediaPipe processing
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image with MediaPipe Hands
    res = capture_hands.process(rgb_image)
    hands = res.multi_hand_landmarks

    if hands:
        for hand in hands:
            # Draw hand landmarks on the image
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark

            for id, lm in enumerate(one_hand_landmarks):
                # Convert normalized coordinates to image coordinates
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                if id == 8:  # Tip of the index finger
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1, y1 = x, y

                    # Visual feedback for the index finger
                    cv2.circle(image, (x, y), 10, (0, 255, 255), -1)

                if id == 4:  # Tip of the thumb
                    x2, y2 = x, y

                    # Visual feedback for the thumb
                    cv2.circle(image, (x, y), 10, (255, 0, 0), -1)

            # Check distance between thumb and index finger for a click
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            if dist < 40:  # Adjusted threshold for better sensitivity
                pyautogui.click()

                # Optional: Visual feedback for a click (green circle)
                cv2.circle(image, (x1, y1), 15, (0, 255, 0), -1)

    # Display the video feed with hand landmarks
    cv2.imshow('Hand movement', image)

    # Exit the loop when 'x' is pressed
    key = cv2.waitKey(1)
    if key == ord('x'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
