from Library import *
from guideline import *

VIDEO_COLOR_WRITER = cv2.VideoWriter('Demo/data/color_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (WIDTH, HEIGHT), isColor = True)
VIDEO_DEPTH_WRITER = cv2.VideoWriter('Demo/data/depth_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (WIDTH, HEIGHT), isColor = True)

def save(pipeline):
    #* 촬영 시작
    print('촬영을 시작합니다')
    
    stime = cv2.getTickCount()  # 시작 시간 기록
    # RGB 프레임을 받아옴
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        while cv2.waitKey(1) < 0:

            frameset = pipeline.wait_for_frames()
            color_frame = frameset.get_color_frame()
            depth_frame = frameset.get_depth_frame()
            
            if not color_frame: continue
        
            # RGB 프레임을 이미지로 변환
            color_image = np.asanyarray(color_frame.get_data())
            depth_iamge = np.asanyarray(depth_frame.get_data())
            
            #가이드 라인 체크
            frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            results = pose.process(frame)
            frame = cv2.bitwise_and(frame, GUIDELINE)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if not INguideline(depth_frame, results): 
                print('가이드라인 안에 들어와주세요')
                return False
            
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            
            cv2.imshow('MediaPipe Pose', cv2.flip(frame, 1))
            
            # 동영상에 프레임을 추가
            VIDEO_COLOR_WRITER.write(cv2.flip(color_image,1))
            VIDEO_DEPTH_WRITER.write(cv2.flip(depth_iamge,1))

            ctime = cv2.getTickCount()  # 현재 시간 기록
            etime = (ctime - stime) / cv2.getTickFrequency()  # 경과 시간 계산

            # 5초가 경과하면 녹화 종료
            if etime > 5:
                break

        # 동영상 저장 종료
        VIDEO_COLOR_WRITER.release()
        VIDEO_DEPTH_WRITER.release()

        print('동영상 저장 완료')
        
    return True
