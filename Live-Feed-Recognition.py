import cv2
from GestureMethods import *

def display_livefeed():
    detected_letters = instantiate_detected_letters_buffer()

    gesture_recogniser = create_gesture_recogniser()
    gesture_point_getter = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
    # Start capturing video from the webcam
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB (OpenCV loads frames in BGR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to an mp.Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Recognize gestures in the image
        gesture_results = gesture_recogniser.recognize(mp_image)
        gesture_points = gesture_point_getter.process(rgb_frame)

        display_hand_landmarks(gesture_points, frame)
        detected_letters = process_points(detected_letters, gesture_results)

        current_letter = current_displayed_letter(detected_letters)
        cv2.putText(frame, f'BSL Letter: {current_letter}',
                    (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        # Show the video feed
        cv2.imshow('Live Feed', frame)
        if current_letter == 'K':
            print(time.time() - start_time)
            time.sleep(1)
        if cv2.waitKey(1) & 0xFF == ord('k'):
            start_time = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_livefeed()


