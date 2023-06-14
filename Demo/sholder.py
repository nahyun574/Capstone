import cv2
import numpy as np
from Library import *
from pathlib import Path

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def Shoulder_incline(x, y, x1, y1):
    # 0 : 평행
    # -1 : 오류
    # 2 : 왼쪽이 높음
    # 3 : 오른쪽이 높음
        if y - y1 == 0: return 0
        elif x - x1 == 0: return -1
        else:
            if (y-y1) / (x-x1) < 0: return 2
            else: return 3

def Shoulder(image,results):
    global Lshoulder_x, Lshoulder_y, Rshoulder_x, Rshoulder_y, Nose_x, Nose_y
        
    if(results.pose_landmarks != None):
        Lshoulder_x, Lshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height
        Rshoulder_x, Rshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height

        Shoulder_result(Lshoulder_x, Lshoulder_y, Rshoulder_x, Rshoulder_y)
                                     
    
def Shoulder_result(lx, ly, rx, ry):
    incline = Shoulder_incline(lx, ly, rx, ry)
        
    if incline == 0 : print('균형')
    elif incline == -1: print('인식 불가')
    elif incline == 2 : print('왼쪽어깨')
    else: print("오른쪽 어깨")   
    
                       

# 동영상 파일 경로
video_path = 'C:/lab/Demo/image/color_output.mp4'

# 동영상 파일 로드
cap = cv2.VideoCapture(video_path)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  i = 0
  while cap.isOpened():
    i+=1
    success, frame = cap.read()
    if(frame.shape != None):
        image_height, image_width, _ = frame.shape

    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)
    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    Shoulder(frame, results)
        
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    cv2.imshow('Output', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
