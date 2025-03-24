import copy
import time
import mediapipe as mp
import numpy as np

def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

def determine_vowel_or_j(palm_marks, index_hand_marks):
    index_point = index_hand_marks[8]
    other_finger_landmarks = [
        palm_marks[4],
        palm_marks[8],
        palm_marks[12],
        palm_marks[16],
        palm_marks[20],
    ]
    # Calculate distances to other fingers
    distances = [calculate_distance(index_point, landmark) for landmark in other_finger_landmarks]
    # Find the index of the closest finger
    closest_finger_index = np.argmin(distances)

    # Map the closest finger to the corresponding letter
    vowel_mapping = {
        0: 'A',  # Thumb
        1: 'E',  # Index
        2: 'I',  # Middle
        3: 'O',  # Ring
        4: 'U'   # Pinky
    }

    return vowel_mapping[closest_finger_index]

def determine_LTR(palm_marks, index_finger_hand):
    index_finger_tip = index_finger_hand[8]
    index_finger_below_tip = index_finger_hand[7]
    middle_ref = copy.deepcopy(palm_marks[9])
    middle_ref.x = 0
    outer_ref = copy.deepcopy(palm_marks[17])
    outer_ref.x = 0

    distance_to_middle = calculate_distance(index_finger_tip, middle_ref)
    distance_to_side = calculate_distance(index_finger_tip, outer_ref)
    if distance_to_side < distance_to_middle:
        if index_finger_tip.y < index_finger_below_tip.y:
            return 'T'
        else:
            return 'R'
    else:
        return 'L'
def determine_KX(hand_1, hand_2):
    if hand_1[5].y > hand_2[6].x:
        return 'K'
    else:
        return 'X'

def add_sign(detected_letters, item):
    i = 0
    # If no sign has been signed or the sign signed has been too quickly detected (i.e a mistake of the model).
    current_letter = ('', time.time())
    if item == '':
        return detected_letters
    if item != 'J' and item != 'H':
        current_letter = calculate_current_letter(detected_letters)
        if time.time() - current_letter[1] < 1:
            return detected_letters
    if item == 'H1' and current_letter[0] == 'H' and time.time() - current_letter[1] < 2:
        return detected_letters
    if item == 'E': # if the sign is a j it may accidentally trigger, so don't register the sign unless its been longer than 2 seconds since last sign.
        current_letter = calculate_current_letter(detected_letters)
        if time.time() - current_letter[1] < 2 and current_letter[0] == 'I':
            return detected_letters

    while i < len(detected_letters):
        if detected_letters[i][2]:
            if detected_letters[i][0] == item and time.time() - detected_letters[i][1] <= 2:
                return detected_letters
            elif detected_letters[i][0] == '':
                detected_letters[i][0] = item
                detected_letters[i][1] = time.time()
                return detected_letters

            detected_letters[i][2] = False

            if i != len(detected_letters) - 1:
                index_to_change = i + 1
            else:
                index_to_change = 0

            detected_letters[index_to_change][0] = item
            detected_letters[index_to_change][1] = time.time()
            detected_letters[index_to_change][2] = True
            return detected_letters
        i += 1
    return detected_letters

def calculate_current_letter(detected_letters):
    i = 0
    current_letter = None
    previous_letter = None

    if detected_letters is None:
        return ''

    while i < len(detected_letters):
        if detected_letters[i][2]:
            current_letter = detected_letters[i]
            previous_letter = detected_letters[i-1]
            break
        i += 1
    if current_letter[0] == 'H1':
        return current_letter
    elif current_letter[0] == 'A':
        if current_letter[1] - previous_letter[1] < 2 and previous_letter[0] == 'I':
            detected_letters = add_sign(detected_letters, 'J')
            return calculate_current_letter(detected_letters)
        else:
            return current_letter
    else:
        return current_letter

def process_points(detected_letters, actual_signs):
    detected_signs = []
    detected_landmarks = []
    if actual_signs.gestures:
        i = 0
        while i < len(actual_signs.gestures):
            detected_signs.append(actual_signs.gestures[i][0].category_name)
            detected_landmarks.append(actual_signs.hand_landmarks[i])
            i += 1
    if len(detected_signs) == 0:
        return detected_letters
    if len(actual_signs.gestures) == 1 and len(actual_signs.hand_landmarks) == 2:
        detected_signs.append('')
        detected_landmarks.append(actual_signs.hand_landmarks[1])
    sign_hierarchy_mapping = {
        ('Circle-Hand', 'Circle-Hand') : 'B',
        ('Circle-Hand', 'Palm-Down') : 'B',
        ('Half-Circle',) : 'C',
        ('Two-Fingers',) : 'F',
        ('Scrunched-Hand', 'Scrunched-Hand') : 'G',
        ('Palm-Down',) : 'H1',
        ('Palm-Side', 'Three-Fingers') : 'M',
        ('Palm-Side', 'Two-Fingers') : 'N',
        ('Hook-Finger',) : 'Q',
        ('F-Cut-Off',) : 'Q',
        ('S-Hands',) : 'S',
        ('Palm-Side', 'V-Fingers') : 'V',
        ('Palm-Up', 'V-Fingers') : 'V',
        ('W-Hands',) : 'W',
        ('V-Fingers',) : 'V',
        ('Y-Finger',) : 'Y',
        ('Palm-Side-Up', 'Z-Hand') : 'Z',
        ('Palm-Up', '$') : 'VOWEL/J',
        ('Pointy-Finger', '$') : 'KX',
        ('Half-Circle', '$') : 'D',
        ('Two-Fingers', '$') : 'F',
        ('F-Cut-Off', '$') : 'F',
        ('S-Hands', '$') : 'S',
        ('Palm-Side', '$') : 'LTR',
        ('Circle-Hand', '$') : 'P',
        ('V-Fingers', '$') : 'V',
        ('Y-Finger', '$') : 'Y'
    }
    signed_letter = ['', None]
    if len(detected_signs) == 2:
        comb1_gestures = detected_signs[0], detected_signs[1]
        comb1_landmarks = detected_landmarks[0], detected_landmarks[1]

        comb2_gestures = detected_signs[1], detected_signs[0]
        comb2_landmarks = detected_landmarks[1], detected_landmarks[0]
    else:
        comb1_gestures = tuple(detected_signs)
        comb2_gestures = comb1_gestures
        comb1_landmarks = detected_landmarks[0]

    for mapping in sign_hierarchy_mapping.keys():
        if len(mapping) == len(detected_signs):
            if comb1_gestures == mapping or comb2_gestures == mapping:
                signed_letter[0] = sign_hierarchy_mapping[mapping]
                signed_letter[1] = comb1_landmarks
                break
            elif '$' in mapping:
                if mapping[0] == comb1_gestures[0]:
                    signed_letter[0] = sign_hierarchy_mapping[mapping]
                    signed_letter[1] = comb1_landmarks
                    break
                elif mapping[0] == comb2_gestures[0]:
                    signed_letter[0] = sign_hierarchy_mapping[mapping]
                    signed_letter[1] = comb2_landmarks
                    break

    hierarchies = ['VOWEL/J', 'LTR', 'W', 'KX']
    if signed_letter[0] not in hierarchies:
        detected_letters = add_sign(detected_letters, signed_letter[0])
    else:
        if len(signed_letter[1]) == 2:
            palm_marks, finger_marks = signed_letter[1]
            if signed_letter[0] == 'VOWEL/J':
                detected_letters = add_sign(detected_letters, determine_vowel_or_j(palm_marks, finger_marks))
            elif signed_letter[0] == 'LTR':
                detected_letters = add_sign(detected_letters, determine_LTR(palm_marks, finger_marks))
            elif signed_letter[0] == 'KX':
                print("RUNNING")
                detected_letters = add_sign(detected_letters, determine_KX(palm_marks, finger_marks))

        elif 'W-Hands' in comb1_gestures or 'Palm-Side' in comb1_gestures:
            current_letter = calculate_current_letter(detected_letters)
            if current_letter != '':
                if current_letter[0] == 'H1' and time.time() - current_letter[1] < 2:
                    detected_letters = add_sign(detected_letters, 'H')
                else:
                    detected_letters = add_sign(detected_letters, signed_letter[0])
    return detected_letters

def display_hand_landmarks(drawn_points, frame):
    mp_drawing = mp.solutions.drawing_utils

    if drawn_points.multi_hand_landmarks and True:
        for hand_landmark in drawn_points.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # Frame to draw on
                hand_landmark,  # Detected hand landmarks
                mp.solutions.hands.HAND_CONNECTIONS,  # Draw connections between landmarks
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),  # Style for landmarks
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)  # Style for connections
            )
    return

def instantiate_detected_letters_buffer():
    detected_letters = [['', time.time() - 1.5, False] for _ in range(5)]
    detected_letters[0][2] = True
    return detected_letters

def current_displayed_letter(detected_letters):
    current_letter_list = calculate_current_letter(detected_letters)
    if current_letter_list == '':
        current_letter = ''
    elif time.time() - current_letter_list[1] > 5 or current_letter_list[0] == 'H1':
        current_letter = ''
    else:
        current_letter = current_letter_list[0]

    return current_letter

def create_gesture_recogniser():
    options = mp.tasks.vision.GestureRecognizerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path='gesture_recognition.task'),
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        min_hand_detection_confidence=0.5,
        num_hands=2)
    return mp.tasks.vision.GestureRecognizer.create_from_options(options)
