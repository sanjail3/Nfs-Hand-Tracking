import cv2 as cv
import mediapipe as mp
from final_control import Control

ob=Control()

mp_draw = mp.solutions.drawing_utils  # Function to Draw Landmarks over Hand
mp_hand = mp.solutions.hands  # Hand Detection Function

fingerTipIds = [4, 8, 12, 16, 20]

# Capturing the Video from the Camera
video = cv.VideoCapture(0)



# Initializing the Hand Detection Function
hands = mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

while True:
    success, image = video.read()

    # Converting the Image to RGB
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    # Processing the Image for Hand Detection
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    # Converting the Image back to BGR
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    # List to store the Landmark's Coordinates
    landmarks_list = []

    current_key_pressed = set()
    keyPressed = False
    keyPressed_lr = False
    recentKey = None

    # If Landmarks Detected i.e., Hand Detected Successfully
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[-1]

        for index, lm in enumerate(hand_landmarks.landmark):
            h, w, c = image.shape  # Height, Width, Channels
            cx, cy = int(lm.x * w), int(lm.y * h)
            landmarks_list.append([index, cx, cy])

        # Drawing the Landmarks for only One Hand
        # Landmarks will be drawn for the Hand which was Detected First
        mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)

    # Stores 1 if finger is Open and 0 if finger is closed
    fingers_open = []

    if len(landmarks_list) != 0:
        for tipId in fingerTipIds:
            if tipId == 4:  # That is the thumb
                if landmarks_list[tipId][1] > landmarks_list[tipId - 1][1]:
                    fingers_open.append(1)
                else:
                    fingers_open.append(0)
            else:
                if landmarks_list[tipId][2] < landmarks_list[tipId - 2][2]:
                    fingers_open.append(1)
                else:
                    fingers_open.append(0)

    # Counts the Number of Fingers Open
    count_fingers_open = fingers_open.count(1)
    control=''

    # If Hand Detected
    if results.multi_hand_landmarks:
        # If All Fingers Closed --> Brake
        if count_fingers_open == 0:

            cv.putText(image, "Reverse", (45, 375), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            control='S'



        # If All Fingers Open --> Gas
        elif count_fingers_open == 5:
            # image[300:425, 20:270] = images['W']
            cv.putText(image, "Accelerator", (45, 375), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            control = 'W'


        # If Palm turned right (Switching condition for left and right)
        elif landmarks_list[17][1] > landmarks_list[0][1]:

            cv.putText(image, "LEFT", (45, 375), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            control = 'A'



        # If Palm turned left
        elif landmarks_list[5][1] < landmarks_list[0][1]:

            cv.putText(image, "RIGHT", (45, 375), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            control = 'D'



        # If Thumb is Up --> Nitro (ALT Key)
        elif fingers_open[3] == 1:

            cv.putText(image, "NITRO", (45, 375), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)


    # If No Hand Detected
    else:
        pass

    ob.startControlling(control)
    cv.imshow("Frame", image)

    # Close the Video if "q" key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv.destroyAllWindows()
