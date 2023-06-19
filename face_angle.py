import cv2
import time
import math #####추가 라이브러리
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
Rlip_y = 0# 입꼬리
upper_lip_x =0
upper_lip_y =0

eye_rad=0
eye_deg=0
lip_rad=0
lip_deg=0
face_rad=0
face_deg=0
eye_lip_rad = 0
eye_lip_deg = 0

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
    global Llip_x, Llip_y, Rlip_x, Rlip_y, upper_lip_x, upper_lip_y# 입꼬리
    global nose_tip_x, nose_tip_y # 코끝
    global glabella_x, glabella_y # 미간
    
    ## 얼굴의 좌표를 받아옴 ##
    if(results_face.multi_face_landmarks != None):
        face_landmarks = results_face.multi_face_landmarks[0]  # 첫 번째 얼굴 랜드마크만 사용
        
        ## 턱 끝 중앙 ##
        chin_landmark = face_landmarks.landmark[152]
        chin_x = int(chin_landmark.x * frame.shape[1])
        chin_y = int(chin_landmark.y * frame.shape[0])
        ## 이마 끝 ##
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
        Llip_x = (Llip_landmark.x * frame.shape[1])
        Llip_y = (Llip_landmark.y * frame.shape[0])
        ## 오른쪽 입꼬리 ##
        Rlip_landmark = face_landmarks.landmark[78]
        Rlip_x = (Rlip_landmark.x * frame.shape[1])
        Rlip_y = (Rlip_landmark.y * frame.shape[0])
        ## 윗입술 중앙 ##
        upper_lip_landmark = face_landmarks.landmark[0]
        upper_lip_x = (upper_lip_landmark.x * frame.shape[1])
        upper_lip_y = (upper_lip_landmark.y * frame.shape[0])
        ## 코끝 ##
        nose_tip_landmark = face_landmarks.landmark[1]
        nose_tip_x = (nose_tip_landmark.x * frame.shape[1])
        nose_tip_y = (nose_tip_landmark.y * frame.shape[0])
        ## 미간 ##
        glabella_landmark = face_landmarks.landmark[168]
        glabella_x = (glabella_landmark.x * frame.shape[1])
        glabella_y = (glabella_landmark.y * frame.shape[0])
            

        # face_incline(glabella_x,glabella_y,upper_lip_x,upper_lip_y)
        # eye_lip_incline(Leye_end_x,Leye_end_y,Reye_end_x,Reye_end_y,Llip_x,Llip_y,Rlip_x,Rlip_y)
        # nose_chin_glabelly(nose_tip_x,nose_tip_y,chin_x,chin_y,glabella_x,glabella_y)
 
    ## 턱과 이마 좌표 알려줌 ##
    if(280 < chin_x < 340 and  400 < chin_y < 420 and 300 < forhead_x < 400 and 53 < forhead_y < 133):
        print(f"chin 좌표: ({chin_x}, {chin_y})")
        print(f"forhead 좌표: ({forhead_x}, {forhead_y})")

## 얼굴 미간-윗입술 과 수직선간의 각도 측정 함수 ## 
def face_angle(glx,gly,ulx,uly):
    global face_rad,face_deg
    
    PI = math.pi
    
    gla = np.array([glx,gly]) 
    ulp = np.array([ulx,uly])
    l1 = np.array([middle_x,middle_y])
    l2 = np.array([middle_x,0])
    
    face = ulp - gla
    line = l1 - l2
    
    norm_face = np.linalg.norm(face)
    norm_line = np.linalg.norm(line)
    
    dot_face = np.dot(face,line)
    face_cos_th = dot_face / (norm_face * norm_line)
    
    face_rad = math.acos(face_cos_th)
    face_deg = math.degrees(face_rad)
    
    # face_deg = round(face_deg,2)
    
    return face_deg
 
## 눈,입과 수직선간이 각도 / 눈과입의 각도 / 얼굴 중심선과 수직선의 각도 를 측정해주는 함수 ##
def eye_lip_angle(lex,ley,rex,rey,llx,lly,rlx,rly):
    global eye_deg,eye_rad,lip_rad,lip_deg
    global eye_lip_deg, eye_lip_rad
    
    PI = math.pi
    
    ll = np.array([llx,lly])
    rl = np.array([rlx,rly])
    le = np.array([lex,ley])
    re = np.array([rex,rey])
    
    l1 = np.array([middle_x,middle_y])
    l2 = np.array([middle_x,0])
    
    eye = le - re
    lip = ll - rl
    line = l1 - l2
    
    norm_eye = np.linalg.norm(eye)
    norm_lip = np.linalg.norm(lip)
    norm_line = np.linalg.norm(line)
    
    dot_eye_line = np.dot(eye,line)
    dot_lip_line = np.dot(lip,line)
    dot_eye_lip = np.dot(eye,lip)
    
    eye_cos_th = dot_eye_line / (norm_eye * norm_line)
    lip_cos_th = dot_lip_line / (norm_lip * norm_line)
    eye_lip_cos_th = dot_eye_lip / (norm_eye * norm_lip)
    
    eye_rad = math.acos(eye_cos_th)
    eye_deg = math.degrees(eye_rad)
    lip_rad = math.acos(lip_cos_th)
    lip_deg = math.degrees(lip_rad)
    eye_lip_rad = math.acos(eye_lip_cos_th)
    eye_lip_deg = math.degrees(eye_lip_rad)
    
    # eye_lip_deg = round(eye_lip_deg,2)
    # eye_deg = round(eye_deg,2)
    # lip_deg = round(lip_deg,2)
    
    return eye_lip_deg, eye_deg, lip_deg
        

## face_angle 로 중앙 안면 비대칭 측정 함수 ##
def face_incline(glx,gly,ulx,uly):
    
    face_results = face_angle(glx,gly,ulx,uly)
    chin = chin_measurement(frame,results)
    
    if face_results < 1 :
        center_face ="대칭"
    elif face_results < 4:
        center_face ="경도"
    elif face_results < 8 :
        center_face ="중등도"
    else :
        center_face ="고도"
        
    return center_face

## eye_lip_angle 로 좌우 안면 비대칭 측정 함수
def eye_lip_incline(lex,ley,rex,rey,llx,lly,rlx,rly):
    
    eye_lip_results ,eye , lip = eye_lip_angle(lex,ley,rex,rey,llx,lly,rlx,rly)
    
    
    if eye_lip_results < 1:
        right_left_face ="대칭"
    elif eye_lip_results < 2:
        right_left_face ="경도"
    elif eye_lip_results < 3:
        right_left_face ="중등도"
    else:
        right_left_face ="고도"
    
    # if 90 <= eye < 91:
    #     if lip < 90 :
    #         face_type ="하악 좌우변위 우측형"
    #     elif lip >= 91 :
    #         face_type ="하악 좌우변위 좌측형"
    # elif eye < 90 :
    #     if lip < 90 :
    #         face_type ="접형골 우측형"
    #     elif lip >= 91 :
    #         face_type ="측두골 좌측형"
    # elif eye >= 91:
    #     if lip < 90 :
    #         face_type ="측두골 우측형"
    #     elif lip >= 91:
    #         face_type ="접형골 좌측형"
            
    return right_left_face #, face_type

def chin_measurement(image,results):
    chin_range = 3 ## 임의로 넣어둔 mm크기
    
    if chin_x < chin_range:
        return 0 ## 근육형 or 대칭으로 분류
    else:
        return 1 ## 턱관절 비대칭으로 분류
    
def FACE_TYPE(image,results): ## 최종 타입 정리 ##
    eye_lip_results ,eye ,lip = eye_lip_angle(Leye_end_x,Leye_end_y,Reye_end_x,Reye_end_y,Llip_x,Llip_y,Rlip_x,Rlip_y) ## 눈과입 각도, 눈/입과 수직선의 각도 ##
    right_left = eye_lip_incline(Leye_end_x,Leye_end_y,Reye_end_x,Reye_end_y,Llip_x,Llip_y,Rlip_x,Rlip_y) ## 좌우변위 중증도 ##
    face = face_incline(glabella_x,glabella_y,upper_lip_x,upper_lip_y) ## 중앙변위 중증도 ##
    chin = chin_measurement(frame,results) ## 턱의 벗어남 유무: 0 대칭 / 1 비대칭 ##
    
    if chin == 0:
        if (lip < 90 and lip >= 91):
            print("턱뼈의 변위는 없는 근육형 불균형 입니다.")
            print("입꼬리가 수직선으로 부터 {}가량 틀어져 있습니다.".format(round(lip,2)))
        else:
            print("대칭의 얼굴입니다.")
    else:
        if (90 <= eye < 91):
            if lip < 90 :
                print("하악 좌우변위 우측형입니다.")
                print("입꼬리가 수직선으로 부터 {}도가량 틀어져 있습니다.".format(round(lip,2)))
            elif lip >= 91 :
                print("하악 좌우변위 좌측형입니다.")
                print("입꼬리가 수직선으로 부터 {}도가량 틀어져 있습니다.".format(round(lip,2)))
        else:
            if (eye < 90):
                if lip < 90 :
                    print("접형골 우측형입니다.")
                    print("눈과 입의 각도가 {}도 틀어져 있습니다.".format(round(eye_lip_results,2)))
                    print("좌우 장면비대칭 중증도는 {}입니다.".format(right_left))
                    print("중앙 안면비대칭 중증도는 {}입니다.".format(face))
                elif lip >= 91 :
                    print("측두골 좌측형입니다.")
                    print("눈과 입의 각도가 {}도 틀어져 있습니다.".format(round(eye_lip_results,2)))
                    print("좌우 장면비대칭 중증도는 {}입니다.".format(right_left))
                    print("중앙 안면비대칭 중증도는 {}입니다.".format(face))
            if(eye >= 91):
                if lip < 90 :
                    print("측두골 우측형입니다.")
                    print("눈과 입의 각도가 {}도 틀어져 있습니다.".format(round(eye_lip_results,2)))
                    print("좌우 장면비대칭 중증도는 {}입니다.".format(right_left))
                    print("중앙 안면비대칭 중증도는 {}입니다.".format(face))
                elif lip >= 91:
                    print("접형골 좌측형입니다.")
                    print("눈과 입의 각도가 {}도 틀어져 있습니다.".format(round(eye_lip_results,2)))
                    print("좌우 장면비대칭 중증도는 {}입니다.".format(right_left))
                    print("중앙 안면비대칭 중증도는 {}입니다.".format(face))
                    
    print(" ")
            
    
## 얼굴에 안내선 그려주는 함수 ##
def Face_line(image,results):
    # 얼굴의 중심 선 #
    cv2.line(frame,(int(upper_lip_x),int(upper_lip_y)),(int(glabella_x),int(glabella_y)),(0,255,0),1)
    ## 수직선 ##
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
    
    ## 기준 선 ##
    cv2.circle(frame,(317,146),5,(255,255,0),-1)

## 코끝, 턱끝, 미간이 수직선과 얼마나 떨어져있는지 측정해주는 함수 ##
def nose_chin_glabelly(nose_tip_x,nose_tip_y,chin_x,chin_y,glabella_x,glabella_y):
    glabelly_area = abs((middle_x - glabella_x) * (0 - glabella_y) - (middle_y - glabella_y) * (middle_x-glabella_x))
    nose_area = abs((middle_x - nose_tip_x) * (0 - nose_tip_y) - (middle_y - nose_tip_y) * (middle_x-nose_tip_x))
    chin_area = abs((middle_x - chin_x) * (0 - chin_y) - (middle_y - chin_y) * (middle_x-chin_x))
    
    line = ((middle_x - middle_x) **2 + (middle_y - 0) **2) **0.5
    
    glabelly_distance = glabelly_area/line
    nose_distance = nose_area/line
    chin_distance = chin_area/line
    
    # print("미간과 수직선의 거리 : ",round(glabelly_distance,2))
    # print("코과 수직선의 거리 : ",round(nose_distance,2))
    print("턱과 수직선의 거리 : ",round(chin_distance,2))
       
#가이드라인 이미지 불러오고 GraySCale, Edge 검출
img = cv2.imread('face_guideline.png')
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
        
        FACE_TYPE(frame,results)
        Face_line(frame,results)
        # mp_drawing.draw_landmarks(
        #     frame,
        #     results.face_landmarks,
        #     mp_holistic.FACEMESH_TESSELATION,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_tesselation_style())

        cv2.imshow('MediaPipe Holistic', cv2.flip(frame, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break


# with mp_holistic.Holistic(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as holistic:

#     face_mesh = mp_face_mesh.FaceMesh(
#         max_num_faces=1,
#         refine_landmarks=True,
#         min_detection_confidence=0.5,
#         min_tracking_confidence=0.5)

#     i=0
    
#     while cv2.waitKey(1) < 0:
#         i+=1
#         frames = pipeline.wait_for_frames()
#         frame  = frames.get_color_frame()
        
#         if not frame: 
#             continue
        
#         frame  = np.asanyarray(frame. get_data())
#         image_height, image_width, _ = frame. shape
        
#         frame. flags.writeable = False
#         frame  = cv2.cvtColor(frame,  cv2.COLOR_BGR2RGB)
        
#         results = holistic.process(frame) 
#         results_face = face_mesh.process(frame) 

#         frame. flags.writeable = True
#         frame  = cv2.cvtColor(frame,  cv2.COLOR_RGB2BGR)
        
#         middle_x = (Lshoulder_x - Rshoulder_x)/2 + Rshoulder_x
#         middle_y = (Lshoulder_y - Rshoulder_y)/2 + Rshoulder_y
        
#         if i == 5:
#             Shoulder(frame, results)
            
#             print("흉골 위치 ({},{})".format(middle_x, middle_y))
#             i = 0
        
#         #Face_measurement(frame,results)
#         #cv2.line(frame,(int(middle_x),int(middle_y)),(int(middle_x),0),(255,255,255),1) #수직 기준선
        
#         mp_drawing.draw_landmarks(
#             frame,
#             results.face_landmarks,
#             mp_holistic.FACEMESH_TESSELATION,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp_drawing_styles
#             .get_default_face_mesh_tesselation_style())

#         cv2.imshow('MediaPipe Holistic', cv2.flip(frame, 1))
        
#         if cv2.waitKey(5) & 0xFF == 27:
#             break
