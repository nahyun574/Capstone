from Library import *
from guideline import *
from save_media import *

#카메라 설정
count = 0
saveon = False
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, 30)

#카메라 ON
pipeline.start(config)
Start_Time = time.time()

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    
    while cv2.waitKey(1) < 0:
        frames = pipeline.wait_for_frames()
        frame = frames.get_color_frame()
        depth = frames.get_depth_frame()
        
        if not frames:
            continue

        #미디어파이프 적용부분
        frame = np.asanyarray(frame.get_data())
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)
        
        #가이드라인 추가
        frame.flags.writeable = True
        frame = cv2.bitwise_and(frame, GUIDELINE)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        #시간체크
        Current_Time = time.time()
        
        
        # #가이드라인 확인 5초마다
        if Current_Time - Start_Time > 2:
            count += 1
            Start_Time = time.time()
            if INguideline(depth, results):
                saveon = save(pipeline)
            
        #*미디어 파이프 그리기
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        cv2.imshow('MediaPipe Pose', cv2.flip(frame, 1)) #좌우반전

        # 종료 조건
        if cv2.waitKey(5) & 0xFF == 27:
            break
        # 타임 아웃
        if count > COUNTOUT or saveon:
            print('횟수 초과')
            break

