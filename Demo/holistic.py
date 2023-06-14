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
mp_face_mesh = mp.solutions.face_mesh

Lshoulder_x = 0
Lshoulder_y = 0
Rshoulder_x = 0
Rshoulder_y = 0

chin_x =0
chin_y=0
forhead_x=0
forhead_y=0


pipeline = rs.pipeline()
config = rs.config()
setWidth = 640
setHeight = 480

inputScale = 1.0/255

config.enable_stream(rs.stream.depth, setWidth, setHeight, rs.format.z16, 30)
config.enable_stream(rs.stream.color, setWidth, setHeight, rs.format.bgr8, 30)
pipeline.start(config)


def Shoulder(image, results):
    global Lshoulder_x, Lshoulder_y, Rshoulder_x, Rshoulder_y
    
    if(results.pose_landmarks != None):
        Lshoulder_x, Lshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height
        Rshoulder_x, Rshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height


def Face(image, results_face):
    global chin_x, chin_y, forhead_x, forhead_y
    
    if(results_face.multi_face_landmarks != None):
        face_landmarks = results_face.multi_face_landmarks[0]  # 첫 번째 얼굴 랜드마크만 사용
        chin_landmark = face_landmarks.landmark[152]
        chin_x = int(chin_landmark.x * frame.shape[1])
        chin_y = int(chin_landmark.y * frame.shape[0])
        
        forhead_landmark = face_landmarks.landmark[10]
        forhead_x = int(forhead_landmark.x * frame.shape[1])
        forhead_y = int(forhead_landmark.y * frame.shape[0])
        #print(frame.shape[1])
        #print(frame.shape[0])
    #print(f"chin 좌표: ({chin_x}, {chin_y})")
    #print(f"forhead 좌표: ({forhead_x}, {forhead_y})")
    
    if(280 < chin_x < 340 and  400 < chin_y < 420 and 300 < forhead_x < 400 and 53 < forhead_y < 133):
        print(f"chin 좌표: ({chin_x}, {chin_y})")
        print(f"forhead 좌표: ({forhead_x}, {forhead_y})")

            
#가이드라인 이미지 불러오고 GraySCale, Edge 검출
img = cv2.imread('C:/lab/Demo/image/face_guideline_head.png')
edges = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
   
pipeline = rs.pipeline()
config = rs.config()
setWidth = 640
setHeight = 480

inputScale = 1.0/255
    
config.enable_stream(rs.stream.depth, setWidth, setHeight, rs.format.z16, 30)
config.enable_stream(rs.stream.color, setWidth, setHeight, rs.format.bgr8, 30)
pipeline.start(config)
    
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:

    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    i = 0
    
    while cv2.waitKey(1) < 0:
        i+=1
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()
           
        if not frame:
            continue
                   
        resize_edges = np.repeat(edges[:,:,np.newaxis],3,-1)
        frame = np.asanyarray(frame.get_data())
        image_height, image_width, _ = frame.shape
            
        # 엣지 추가
        frame = cv2.bitwise_and(frame, resize_edges)
            
        frame.flags.writeable = False
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = holistic.process(frame) 
        results_face = face_mesh.process(frame) 

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
        if i == 5:
            Shoulder(frame, results)
            Face(frame, results_face)
            i = 0
                
        middle_x = (Lshoulder_x - Rshoulder_x)/2 + Rshoulder_x
        middle_y = (Lshoulder_y - Rshoulder_y)/2 + Rshoulder_y
        
        if i == 5:
            Shoulder(frame, results)
            print("흉골 위치 ({},{})".format(middle_x, middle_y))
            i = 0
        
            
        cv2.line(frame,(int(middle_x),int(middle_y)),(int(middle_x),0),(255,255,255),1)
        
        mp_drawing.draw_landmarks(
            frame,
            results.face_landmarks,
            mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())

        cv2.imshow('MediaPipe Holistic', cv2.flip(frame, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break


with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:

    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    i=0
    
    while cv2.waitKey(1) < 0:
        i+=1
        frames = pipeline.wait_for_frames()
        frame  = frames.get_color_frame()
        
        if not frame: 
            continue
        
        frame  = np.asanyarray(frame. get_data())
        image_height, image_width, _ = frame. shape
        
        frame. flags.writeable = False
        frame  = cv2.cvtColor(frame,  cv2.COLOR_BGR2RGB)
        
        results = holistic.process(frame) 
        results_face = face_mesh.process(frame) 

        frame. flags.writeable = True
        #frame  = cv2.cvtColor(frame,  cv2.COLOR_RGB2BGR)
        
        middle_x = (Lshoulder_x - Rshoulder_x)/2 + Rshoulder_x
        middle_y = (Lshoulder_y - Rshoulder_y)/2 + Rshoulder_y
        
        if i == 5:
            Shoulder(frame, results)
            
            print("흉골 위치 ({},{})".format(middle_x, middle_y))
            i = 0
        
            
        cv2.line(frame,(int(middle_x),int(middle_y)),(int(middle_x),0),(255,255,255),1)
        
        mp_drawing.draw_landmarks(
            frame,
            results.face_landmarks,
            mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())

        cv2.imshow('MediaPipe Holistic', cv2.flip(frame, 1))
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

