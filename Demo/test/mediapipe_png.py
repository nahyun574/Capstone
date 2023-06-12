import cv2
import numpy as np
import mediapipe as mp
from pathlib import Path

# PNG 이미지 파일 경로
image_path = 'F:/backup/Project/CapStone/code/Demo/test/2.png'

# 이미지 파일 로드
frame = cv2.imread(image_path)

frameWidth = frame.shape[1]
frameHeight = frame.shape[0]

# MediaPipe Pose 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(static_image_mode=True) as pose:
    # 이미지를 RGB로 변환
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # MediaPipe에 입력
    results = pose.process(frame_rgb)

    # 스켈레톤 그리기
    if results.pose_landmarks:
        # 스켈레톤 그리기 함수 사용
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))
    
    # 결과 이미지를 다시 BGR로 변환
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # 결과 이미지 출력
    cv2.imshow('Output-Keypoints', frame_bgr)
    cv2.imwrite(image_path[:-5] + 'mediapipe.png',frame_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
