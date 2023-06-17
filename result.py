from Library import *

def Shoulder_incline(lx, ly, rx, ry):
    # 0 : 평행
    # -1 : 오류
    # 2 : 왼쪽이 높음
    # 3 : 오른쪽이 높음
    if 0 <= (ly - ry) <= 1: 
        R_TEXT.guide = '균형'
    elif lx - rx == 0:
        R_TEXT.guide = '인식불가'
    else:
        if (ry-ly) / (rx-lx) > 0:
            if abs(ry-ly) > 2:
                R_TEXT.guide = '왼쪽어깨'
                R_TY_TEXT.guide = '고도 비대칭'
            elif abs(ry-ly) > 1.5:
                R_TEXT.guide = '왼쪽어깨'
                R_TY_TEXT.guide = '중도 비대칭'
            else:
                R_TEXT.guide = '왼쪽어깨'
                R_TY_TEXT.guide = '경도 비대칭'
            
        else:
            if abs(ry-ly) > 2:
                R_TEXT.guide = '오른쪽어깨'
                R_TY_TEXT.guide = '고도 비대칭' 
            elif abs(ry-ly) > 1.5:
                R_TEXT.guide = '오른쪽어깨'
                R_TY_TEXT.guide = '중도 비대칭' 
            else:
                R_TEXT.guide = '오른쪽어깨'
                R_TY_TEXT.guide = '경도 비대칭'  

#어깨 결과 측정
def Shoulder(Landmarks):
    L_SHOULDER.x, L_SHOULDER.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * HEIGHT
    R_SHOULDER.x, R_SHOULDER.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * HEIGHT
    
    SUM_LS.x += L_SHOULDER.x
    SUM_LS.y += L_SHOULDER.y
    SUM_RS.x += R_SHOULDER.x
    SUM_RS.y += R_SHOULDER.y

def Sum_Sholder(i):
    SUM_LS.x = SUM_LS.x / float(i-1)
    SUM_LS.y = SUM_LS.y / float(i-1)
    SUM_RS.x = SUM_RS.x / float(i-1)
    SUM_RS.y = SUM_RS.y / float(i-1) 
                
    Shoulder_incline(SUM_LS.x, SUM_LS.y, SUM_RS.x, SUM_RS.y)
                
def Video_result():   
    # 동영상 파일 경로
    video_path = 'C:/lab/Demo/image/color_output.mp4'

    # 동영상 파일 로드
    cap = cv2.VideoCapture(video_path)

    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        i = 0
        while cap.isOpened():
            i+=1
            success, frame = cap.read()
            try:
                if not success or frame.shape is not None:
            
                    HEIGHT, WIDTH, _ = frame.shape

                    frame.flags.writeable = False
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    MP_landmark = pose.process(frame)
                    frame.flags.writeable = True
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    Shoulder(MP_landmark)
                        
                    mp_drawing.draw_landmarks(
                        frame,
                        MP_landmark.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                    
                    cv2.imshow('Output', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            except:
                Sum_Sholder(i)

                cv2.destroyAllWindows()
                break

        cap.release()
            
