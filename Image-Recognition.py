import cv2
from GestureMethods import *
import mediapipe as mp


def process_image(image_path):
    detected_letters = instantiate_detected_letters_buffer()

    # Load the image using OpenCV
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Unable to load image from {image_path}.")
        return

    # Convert the frame to RGB (OpenCV loads images in BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    gesture_recogniser = create_gesture_recogniser()
    gesture_point_getter = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2,
                                                    min_detection_confidence=0.3)

    # Convert the frame to an mp.Image object
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Recognize gestures in the image
    gesture_results = gesture_recogniser.recognize(mp_image)
    gesture_points = gesture_point_getter.process(rgb_frame)

    # Display hand landmarks on the frame
    display_hand_landmarks(gesture_points, frame)

    # Process detected gestures
    detected_letters = process_points(detected_letters, gesture_results)
    current_letter = current_displayed_letter(detected_letters)

    # Overlay the detected letter on the image
    cv2.putText(frame, f'BSL Letter: {current_letter}',
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    # Display the final image
    cv2.imshow('Processed Image', frame)
    print(f'Detected Letter: {current_letter}')

    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Example usage
image_path = input("Enter the path to the image: ")
process_image(image_path)
