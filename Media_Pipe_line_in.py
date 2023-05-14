import cv2
import mediapipe as mp
import numpy as np
import pyfps
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

lsx_li = []
lsy_li = []
rsx_li = []
rsy_li = []

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
  #좌표 구하기
  #Lshoulder_x, Lshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height
  #Rshoulder_x, Rshoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height
  #Lear_x, Lear_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].y * image_height
  #Rear_x, Rear_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].x * image_width, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].y * image_height
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

        if(len(rsy_li) == 5):
          Ls_x = sum(lsx_li) / 5
          Ls_y = sum(lsy_li) / 5
          Rs_x = sum(rsx_li) / 5
          Rs_y = sum(rsy_li) / 5
          Shoulder_result(Ls_x,Ls_y,Rs_x,Rs_y)
          lsx_li.clear()
          lsy_li.clear()
          rsx_li.clear()
          rsy_li.clear()
          #5번 찍으면 평균 구함
      else:
        print("가이드라인 안에 들어와주세요")
    
  else:
    print("카메라 앞에 바르게 서주세요")
    #값 안들어오면 메세지
  
def Shoulder_result(lx, ly, rx, ry):
    incline = Shoulder_incline(lx,ly,rx,ry)
    if incline == 0 : print('균형')
    elif incline == -1: print('인식 불가')
    elif incline == 2 : print('왼쪽어깨')
    else: print("오른쪽 어깨")


# # For static images:
# IMAGE_FILES = []
# BG_COLOR = (192, 192, 192) # gray
# with mp_pose.Pose(
#     static_image_mode=True,
#     model_complexity=2,
#     enable_segmentation=True,
#     min_detection_confidence=0.5) as pose:
#   for idx, file in enumerate(IMAGE_FILES):
#     image = cv2.imread(file)
#     image_height, image_width, _ = image.shape
#     # Convert the BGR image to RGB before processing.
#     results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     if not results.pose_landmarks:
#       continue
#     print(
#         f'Nose coordinates: ('
#         f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
#         f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
#     )

#     annotated_image = image.copy()
#     # Draw segmentation on the image.
#     # To improve segmentation around boundaries, consider applying a joint
#     # bilateral filter to "results.segmentation_mask" with "image".
#     condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
#     bg_image = np.zeros(image.shape, dtype=np.uint8)
#     bg_image[:] = BG_COLOR
#     annotated_image = np.where(condition, annotated_image, bg_image)
#     # Draw pose landmarks on the image.
#     mp_drawing.draw_landmarks(
#         annotated_image,
#         results.pose_landmarks,
#         mp_pose.POSE_CONNECTIONS,
#         landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
#     # Plot pose world landmarks.
#     mp_drawing.plot_landmarks(
#         results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

#가이드라인 이미지 불러오고 GraySCale, Edge 검출
img = cv2.imread('guideline.png')
edges = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(gray,50,150,apertureSize=3)

#Egdge 반전
#edges = 255 - edges

# For webcam input:
cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS) #웹 캠에서 fps값 획득

if fps == 0.0:
    fps = 30.0

time_per_frame_video = 1 / fps
last_time = time.perf_counter()

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  i = 0
  while cap.isOpened():
    i+=1
    success, image = cap.read()
    image_height, image_width, _ = image.shape
    #print(image_height, image_width)
    # if not success:
    #   print("Ignoring empty camera frame.")
    #   # If loading a video, use 'break' instead of 'continue'.
    #   continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    
    resize_edges = np.repeat(edges[:,:,np.newaxis],3,-1)
    
    # 엣지 추가
    image = cv2.bitwise_and(image, resize_edges)
    
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #어깨 좌표 구하는 함수
    if i == 50:
      Shoulder(image,results)
      i = 0
      
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    
    pyfps.ShowFPS(image,last_time,time_per_frame_video)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
