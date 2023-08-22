import cv2
import mediapipe as mp
import numpy as np
import math
from pynput.keyboard import Key, Controller

import time

keyboard = Controller()
class Deteccion:
    def __init__(self,dir,acel):
        self.direccion = round(dir,2)
        self.aceleracion = round(acel,2)
        
        
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

with open("values.txt", "w") as valores:
  valores.write("")
# For webcam input:

cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    try:
      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      
      results = pose.process(image)

    
      image_width = image.shape[0] 
      image_height = image.shape[1] 
      # Draw the pose annotation on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      

      mp_drawing.draw_landmarks(
          image,
          results.pose_landmarks,
          mp_pose.POSE_CONNECTIONS,
          landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
      
      Shoulder = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width,results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height]
      Right_wrist = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width,results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height]
      
      LeftShoulder = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width,results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height]
      Left_wrist = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width,results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height]
      

      
      direccion = Right_wrist[0]-Shoulder[0]
      acceleracion = Left_wrist[1]-LeftShoulder[1]
      #print(direccion,acceleracion)
      posiciones = Deteccion(direccion,acceleracion)
      # Flip the image horizontally for a selfie-view display.
      
      mov = True
      if mov == True:
        try:
            try:
                if acceleracion < 0:
                    keyboard.press(Key.up)
                else:
                    keyboard.release(Key.up)
                if acceleracion > 100:
                    keyboard.press(Key.down)
                else:
                    keyboard.release(Key.down)
                if direccion < -80:
                    keyboard.press(Key.right)
                else:
                    keyboard.release(Key.right)
                if direccion > -60:
                    keyboard.press(Key.left)
                else:
                    keyboard.release(Key.left)
            except IndexError:
                pass
        except ValueError:
            pass
      cv2.imshow('concat_vertical', image)
      if cv2.waitKey(5) & 0xFF == 27:
        break
    except AttributeError:
      pass
cap.release()