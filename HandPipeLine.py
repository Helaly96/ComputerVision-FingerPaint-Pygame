import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
ImageCounter= 0
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
PointsToDraw= []
while cap.isOpened():
  success, image = cap.read()
  if not success:
    print("Ignoring empty camera frame.")
    # If loading a video, use 'break' instead of 'continue'.
    continue

  # Flip the image horizontally for a later selfie-view display, and convert
  # the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  TempImage= np.zeros((image.shape)).astype('float32')

  H,W,_ = image.shape
  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  results = hands.process(image)
  # Draw the hand annotations on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      XPixel_IndexFinger= hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * W
      YPixel_IndexFinger= hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * H

      XPixel_MiddleFinger= hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * W
      YPixel_MiddleFinger= hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * H

      cv2.circle(image, (int(XPixel_IndexFinger),int(YPixel_IndexFinger)), 20, (255, 0, 0), -1)
      cv2.circle(image, (int(XPixel_MiddleFinger),int(YPixel_MiddleFinger)), 20, (0, 0, 255), -1)
      dist= abs(np.linalg.norm(np.array([XPixel_IndexFinger,YPixel_IndexFinger])-np.array([XPixel_MiddleFinger,YPixel_MiddleFinger])))

      if (dist<90):
        PointsToDraw.append([int(XPixel_MiddleFinger),int(YPixel_MiddleFinger)])
      else:
        PointsToDraw=[]

      for i in range(len(PointsToDraw)):
        cv2.circle(TempImage, tuple(PointsToDraw[i]), 20, (255, 0, 0), -1)

      # print("Distance between the 2 fingers"+str(dist))
      mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
  cv2.imshow('MediaPipe Hands', image)
  cv2.imshow('Canvas', TempImage)
  k= cv2.waitKey(27)
  if k & 0xFF == 27:
    break
  elif k == ord('e'):
    cv2.imwrite(str(ImageCounter)+".jpg",TempImage)
    print("!!")

hands.close()
cap.release()