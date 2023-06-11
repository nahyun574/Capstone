import cv2
import time
import numpy as np
import pandas as pd
import mediapipe as mp
import pyrealsense2 as rs
from multiprocessing import Process
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

Lshoulder_x = 0
Lshoulder_y = 0
Rshoulder_x = 0
Rshoulder_y = 0

lsx_li = []
lsy_li = []
rsx_li = []
rsy_li = []

pipeline = rs.pipeline()
config = rs.config()
setWidth = 640
setHeight = 480

inputScale = 1.0/255

#config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, setWidth, setHeight, rs.format.bgr8, 30)
pipeline.start(config)


def Shoulder(image,results):
    global Lshoulder_x, Lshoulder_y, Rshoulder_x, Rshoulder_y
    
    if(results.pose_landmarks != None):
        Lshoulder_x, Lshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height
        Rshoulder_x, Rshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height
        Lear_x, Lear_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].y * image_height
        Rear_x, Rear_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].y * image_height
    
        if(148 < Lshoulder_x < 496 and 265 < Lshoulder_y < 480 and 148 < Rshoulder_x < 496 and 265 < Rshoulder_y < 480):
            if(258 < Lear_x < 374 and 109 < Lear_y < 183 and 258 < Rear_x < 374 and 109 < Rear_y < 183):
                print("left shoulder : ", Lshoulder_x, Lshoulder_y)
                
                lsx_li.append(Lshoulder_x)
                lsy_li.append(Lshoulder_y)

                print("right shoulder : ", Rshoulder_x, Rshoulder_y)
                
                rsx_li.append(Rshoulder_x)
                rsy_li.append(Rshoulder_y)

with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:

    i=0
    while cv2.waitKey(1) < 0:
        i+=1
        frames = pipeline.wait_for_frames()
        image = frames.get_color_frame()
        
        if not image:
            continue
        
        image = np.asanyarray(image.get_data())
        image_height, image_width, _ = image.shape
        
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        middle_x = (Lshoulder_x - Rshoulder_x)/2 + Rshoulder_x
        middle_y = (Lshoulder_y - Rshoulder_y)/2 + Rshoulder_y
        
        if i == 10:
            Shoulder(image,results)
            print("왼쪾 위치 at pixel ({}, {})".format(Lshoulder_x, Lshoulder_y))
            print("오른쪾 위치 at pixel ({}, {})".format(Rshoulder_x, Rshoulder_y,))
            print("흉골위치 ({},{})".format(middle_x,middle_y))
            i = 0
        
        cv2.line(image,(int(middle_x),int(middle_y)),(int(middle_x),0),(255,255,255),1)
        
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())

        cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
