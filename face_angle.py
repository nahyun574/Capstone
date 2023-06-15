import cv2
import time
import math #####추가 라이브러리#####
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
middle_x = 0
middle_y = 0

chin_x =0
chin_y=0
forhead_x=0
forhead_y=0

Leye_end_x = 0
Leye_end_y = 0
Leye_front_x = 0
Leye_front_y = 0
Reye_end_x = 0
Reye_end_y =0 
Reye_front_x =0
Reye_front_y =0 #눈

Llip_x =0
Llip_y =0
Rlip_x =0
Rlip_y = 0# 입

eye_rad=0
eye_deg=0
lip_rad=0
lip_deg=0

nose_tip_x =0 
nose_tip_y =0 # 코끝

glabella_x =0
glabella_y =0 # 미간

pipeline = rs.pipeline()
config = rs.config()
setWidth = 640
setHeight = 480

inputScale = 1.0/255

config.enable_stream(rs.stream.depth, setWidth, setHeight, rs.format.z16, 30)
config.enable_stream(rs.stream.color, setWidth, setHeight, rs.format.bgr8, 30)
pipeline.start(config)


def Shoulder(image, results):
    global Lshoulder_x, Lshoulder_y, Rshoulder_x, Rshoulder_y,middle_x,middle_y
    
    if(results.pose_landmarks != None):
        Lshoulder_x, Lshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height
        Rshoulder_x, Rshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height

        middle_x = (Lshoulder_x - Rshoulder_x)/2 + Rshoulder_x
        middle_y = (Lshoulder_y - Rshoulder_y)/2 + Rshoulder_y
        
        #print("left shoulder : ", Lshoulder_x, Lshoulder_y)
        #print("right shoulder : ", Rshoulder_x, Rshoulder_y)

def Face(image, results):
    global chin_x, chin_y, forhead_x, forhead_y
    global Leye_end_x, Leye_end_y, Leye_front_x, Leye_front_y, Reye_end_x, Reye_end_y, Reye_front_x, Reye_front_y #눈
    global Llip_x, Llip_y, Rlip_x, Rlip_y # 입꼬리
    global nose_tip_x, nose_tip_y # 코끝
    global glabella_x, glabella_y # 미간
    
    if(results_face.multi_face_landmarks != None):
        face_landmarks = results_face.multi_face_landmarks[0]  # 첫 번째 얼굴 랜드마크만 사용
        chin_landmark = face_landmarks.landmark[152]
        chin_x = int(chin_landmark.x * frame.shape[1])
        chin_y = int(chin_landmark.y * frame.shape[0])
        
        forhead_landmark = face_landmarks.landmark[10]
        forhead_x = int(forhead_landmark.x * frame.shape[1])
        forhead_y = int(forhead_landmark.y * frame.shape[0])
        
        ## 왼쪽눈 눈꼬리 ##
        Leye_end_landmark = face_landmarks.landmark[263]
        Leye_end_x = int(Leye_end_landmark.x * frame.shape[1])
        Leye_end_y = int(Leye_end_landmark.y * frame.shape[0])
        ## 왼쪽눈 눈앞머리 ##
        Leye_front_landmark = face_landmarks.landmark[362]
        Leye_front_x = int(Leye_front_landmark.x * frame.shape[1])
        Leye_front_y = int(Leye_front_landmark.y * frame.shape[0])
        ## 오른쪽눈 눈꼬리 ##
        Reye_end_landmark = face_landmarks.landmark[33]
        Reye_end_x = int(Reye_end_landmark.x * frame.shape[1])
        Reye_end_y = int(Reye_end_landmark.y * frame.shape[0])
        ## 오른쪽눈 눈앞머리 ##
        Reye_front_landmark = face_landmarks.landmark[133]
        Reye_front_x = int(Reye_front_landmark.x * frame.shape[1])
        Reye_front_y = int(Reye_front_landmark.y * frame.shape[0])
        
        ## 왼쪽 입꼬리 ##
        Llip_landmark = face_landmarks.landmark[308]
        Llip_x = int(Llip_landmark.x * frame.shape[1])
        Llip_y = int(Llip_landmark.y * frame.shape[0])
        ## 오른쪽 입꼬리 ##
        Rlip_landmark = face_landmarks.landmark[78]
        Rlip_x = int(Rlip_landmark.x * frame.shape[1])
        Rlip_y = int(Rlip_landmark.y * frame.shape[0])
        ## 코끝 ##
        nose_tip_landmark = face_landmarks.landmark[1]
        nose_tip_x = int(nose_tip_landmark.x * frame.shape[1])
        nose_tip_y = int(nose_tip_landmark.y * frame.shape[0])
        ## 미간 ##
        glabella_landmark = face_landmarks.landmark[6]
        glabella_x = int(glabella_landmark.x * frame.shape[1])
        glabella_y = int(glabella_landmark.y * frame.shape[0])
        
        face_eye_angle(Leye_end_x,Leye_end_y,Reye_end_x,Reye_end_y,Llip_x,Llip_y,Rlip_x,Rlip_y)
        nose_chin_glabelly(nose_tip_x,nose_tip_y,chin_x,chin_y,glabella_x,glabella_y)
 
    #print(f"chin 좌표: ({chin_x}, {chin_y})")
    #print(f"forhead 좌표: ({forhead_x}, {forhead_y})")
    
    if(280 < chin_x < 340 and  400 < chin_y < 420 and 300 < forhead_x < 400 and 53 < forhead_y < 133):
        print(f"chin 좌표: ({chin_x}, {chin_y})")
        print(f"forhead 좌표: ({forhead_x}, {forhead_y})")
        
def Face_line(image,results): ## 얼굴에 선, 점 찍는 함수 ##
    cv2.line(frame,(int(middle_x),int(middle_y)),(int(middle_x),0),(255,255,255),1)
        
    ##  눈 직선긋기 ##
    cv2.line(frame,(int(Leye_end_x),int(Leye_end_y)),(int(Reye_end_x),int(Reye_end_y)),(255,0,255),2)
    ## 입꼬리 직선 긋기 ##
    cv2.line(frame,(int(Llip_x),int(Llip_y)),(int(Rlip_x),int(Rlip_y)),(255,0,255),2)
    # 코 점 #
    cv2.circle(frame,(int(nose_tip_x),int(nose_tip_y)),5,(255,0,0),-1)
    # 미간 점 #
    cv2.circle(frame,(int(glabella_x),int(glabella_y)),5,(255,0,0),-1)
    # 턱끝 점 #
    cv2.circle(frame,(int(chin_x),int(chin_y)),5,(255,0,0),-1)
    

def face_eye_angle(lex,ley,rex,rey,llx,lly,rlx,rly): ## 눈하고 입꼬리 수직선과 각도 구하는 함수 ##
    global eye_deg,eye_rad,lip_rad,lip_deg
    
    PI = math.pi
    le = np.array([lex,ley])
    re = np.array([rex,rey])
    l1 = np.array([middle_x,middle_y])
    l2 = np.array([middle_x,0])
    ll = np.array([llx,lly])
    rl = np.array([rlx,rly])
    
    eye = le - re
    lip = ll - rl
    line = l1 - l2
    
    norm_eye = np.linalg.norm(eye)
    norm_lip = np.linalg.norm(lip)
    norm_line = np.linalg.norm(line)
    
    dot_eye_line = np.dot(eye,line)
    dot_lip_line = np.dot(lip,line)
    
    eye_cos_th = dot_eye_line / (norm_eye * norm_line)
    lip_cos_th = dot_lip_line / (norm_lip * norm_line)
    
    eye_rad = math.acos(eye_cos_th)
    eye_deg = math.degrees(eye_rad)
    lip_rad = math.acos(lip_cos_th)
    lip_deg = math.degrees(lip_rad)
    
    print("eye :", 180 - int(eye_deg))
    print("lip :", 180 - int(lip_deg))
    
def nose_chin_glabelly(nose_tip_x,nose_tip_y,chin_x,chin_y,glabella_x,glabella_y): ## 미간, 코끝, 턱끝이 수직선과의 거리 측정 함수 ##
  
    glabelly_area = abs((middle_x - glabella_x) * (0 - glabella_y) - (middle_y - glabella_y) * (middle_x-glabella_x))
    nose_area = abs((middle_x - nose_tip_x) * (0 - nose_tip_y) - (middle_y - nose_tip_y) * (middle_x-nose_tip_x))
    chin_area = abs((middle_x - chin_x) * (0 - chin_y) - (middle_y - chin_y) * (middle_x-chin_x))
    
    line = ((middle_x - middle_x) **2 + (middle_y - 0) **2) **0.5
    
    glabelly_distance = glabelly_area/line
    nose_distance = nose_area/line
    chin_distance = chin_area/line
    
    print("미간과 수직선의 거리 : ",round(glabelly_distance,2))
    print("코과 수직선의 거리 : ",round(nose_distance,2))
    print("턱과 수직선의 거리 : ",round(chin_distance,2))
    
      