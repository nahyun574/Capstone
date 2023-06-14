from Library import *
from guideline import *
#from save_media import *

def GuideText(frame):
    #텍스트 위치 계산
    text_x, text_y = int((HEIGHT - len(STR.guide)*7) / 2), 40 #가로 중앙으로 설정

    frame = Image.fromarray(frame)
    ImageDraw.Draw(frame).text((text_x,text_y), STR.guide, font=FONT, fill=GREEN)

    frame = np.array(frame)
    return frame

def video(cam_label):
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        
            time.sleep(1)
            frames = PIPELINE.wait_for_frames()
            depth_frames = ALIGN.process(frames)
            frame = frames.get_color_frame()
            depth = depth_frames.get_depth_frame()

            frame = cv2.cvtColor(np.asanyarray(frame.get_data()), cv2.COLOR_BGR2RGB)

            MP_landmark = pose.process(frame)

            #*미디어 파이프 그리기
            mp_drawing.draw_landmarks(
                frame,
                MP_landmark.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

            #가이드 라인 추가 및 텍스트 설정
            #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame,1)
            frame = cv2.bitwise_and(frame,GUIDELINE)
            frame = GuideText(frame)
            
            #화면 표시
            img = Image.fromarray(frame) # Image 객체로 변환
            imgtk = ImageTk.PhotoImage(image=img) # ImageTk 객체로 변환
            # OpenCV 동영상
        
            cam_label.imgtk = imgtk
            cam_label.configure(image=imgtk)
            time.sleep(0.1)
            video(cam_label)

def face_video(cam_label):
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
            time.sleep(1)
            frames = PIPELINE.wait_for_frames()

            frame = frames.get_color_frame()

            frame = cv2.cvtColor(np.asanyarray(frame.get_data()), cv2.COLOR_BGR2RGB)

            HO_landmark = holistic.process(frame) 
            FC_landmark = face_mesh.process(frame) 

            #*미디어 파이프 그리기
            mp_drawing.draw_landmarks(
                frame,
                HO_landmark.face_landmarks,
                mp_holistic.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style()
            )
            
            #가이드 라인 추가 및 텍스트 설정
            #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame,1)
            frame = cv2.bitwise_and(frame,GUIDELINE)
            frame = GuideText(frame)
            
            #화면 표시
            img = Image.fromarray(frame) # Image 객체로 변환
            imgtk = ImageTk.PhotoImage(image=img) # ImageTk 객체로 변환
            # OpenCV 동영상
        
            cam_label.imgtk = imgtk
            cam_label.configure(image=imgtk)
            time.sleep(0.1)
            face_video(cam_label)


def Media_Shoulder():
    count = 0
    saveon = False
    Start_Time = time.time()

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cv2.waitKey(1) < 0:
            frames = PIPELINE.wait_for_frames()
            depth_frames = ALIGN.process(frames)
            frame = frames.get_color_frame()
            depth = depth_frames.get_depth_frame()

            if not frame or not depth:
                continue

            frame = cv2.cvtColor(np.asanyarray(frame.get_data()), cv2.COLOR_BGR2RGB)

            MP_landmark = pose.process(frame)

            # #가이드라인 확인 5초마다
            if time.time() - Start_Time > N_SECONDS:
                count += 1
                Start_Time = time.time()

                if INguideline(depth, MP_landmark):
                    saveon = save()

            #*미디어 파이프 그리기
            mp_drawing.draw_landmarks(
                frame,
                MP_landmark.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

        
            #가이드 라인 추가 및 텍스트 설정
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame,1)
            frame = cv2.bitwise_and(frame,GUIDELINE)
            frame = GuideText(frame)
            
            #화면 표시
            cv2.imshow("", frame)

            # 종료 조건
            if cv2.waitKey(5) & 0xFF == 27:
                break
            
            # 타임 아웃
            if count > COUNTOUT:
                break
            
            if saveon:
                #저장완료
                break
        
def Media_Face():
    count = 0
    saveon = False
    Start_Time = time.time()

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        while cv2.waitKey(1) < 0:
            frames = PIPELINE.wait_for_frames()
            depth_frames = ALIGN.process(frames)
            frame = frames.get_color_frame()
            depth = depth_frames.get_depth_frame()

            if not frame:
                continue

            frame = cv2.cvtColor(np.asanyarray(frame.get_data()), cv2.COLOR_BGR2RGB)

            HO_landmark = holistic.process(frame) 
            FC_landmark = face_mesh.process(frame) 
        
            # #가이드라인 확인 5초마다
            if time.time() - Start_Time > N_SECONDS:
                count += 1
                Start_Time = time.time()

                if INFace(depth, FC_landmark):
                    saveon = face_save()
            
            #*미디어 파이프 그리기
            mp_drawing.draw_landmarks(
            frame,
            HO_landmark.face_landmarks,
            mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style()
            )

        
            #가이드 라인 추가 및 텍스트 설정
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame,1)
            frame = cv2.bitwise_and(frame,FACE_GUIDELINE)
            frame = GuideText(frame)
            
            #화면 표시
            cv2.imshow("", frame)

            # 종료 조건
            if cv2.waitKey(5) & 0xFF == 27:
                break
            
            # 타임 아웃
            if count > COUNTOUT:
                break
            
            if saveon:
                #저장완료
                break
      
        
############## SAVE MEDIA #################

VIDEO_COLOR_WRITER = cv2.VideoWriter('C:/lab/Demo/image/color_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (WIDTH, HEIGHT), isColor = True)
VIDEO_DEPTH_WRITER = cv2.VideoWriter('C:/lab/Demo/image/depth_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (WIDTH, HEIGHT), isColor = True)

FACEVIDEO_COLOR_WRITER = cv2.VideoWriter('C:/lab/Demo/image/face_color_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (WIDTH, HEIGHT), isColor = True)

def save():
    #* 촬영 시작
    STR.guide = '촬영을 시작합니다 3'
    
    stime = cv2.getTickCount()  # 시작 시간 기록
    # RGB 프레임을 받아옴
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        while cv2.waitKey(1) < 0:

            frames = PIPELINE.wait_for_frames()
            depth_frames = ALIGN.process(frames)
            color_frame = frames.get_color_frame()
            depth_frame = depth_frames.get_depth_frame()
            
            if not color_frame: continue
        
            # RGB 프레임을 이미지로 변환
            color_image = np.asanyarray(color_frame.get_data())
            depth_iamge = np.asanyarray(depth_frame.get_data())
            
            #가이드 라인 체크
            frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            results = pose.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.bitwise_and(frame, GUIDELINE)
            
            if not INguideline(depth_frame, results):
                STR.guide = "가이드라인 안에 들어와주세요"
                return False
            
            frame = cv2.flip(frame,1)
            frame = GuideText(frame)
            cv2.imshow("", frame)


            ctime = cv2.getTickCount()  # 현재 시간 기록
            etime = (ctime - stime) / cv2.getTickFrequency()  # 경과 시간 계산


            # 5초가 경과하면 녹화 종료
            if 1 < etime < 2:
                STR.guide = '촬영을 시작합니다 2'
            elif 2 < etime < 3:
                STR.guide = '촬영을 시작합니다 1'
                
            # 동영상에 프레임을 추가
            elif etime > 3:
                STR.guide = "촬영중입니다. 움직이지마세요."
                VIDEO_COLOR_WRITER.write(cv2.flip(color_image,1))
                VIDEO_DEPTH_WRITER.write(cv2.flip(depth_iamge,1))
            if etime > 7:
                break

        # 동영상 저장 종료
        VIDEO_COLOR_WRITER.release()
        VIDEO_DEPTH_WRITER.release()

        print('동영상 저장 완료')
        
    return True

def face_save():
    #* 촬영 시작
    STR.guide = '촬영을 시작합니다 3'
    
    stime = cv2.getTickCount()  # 시작 시간 기록
    # RGB 프레임을 받아옴
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        while cv2.waitKey(1) < 0:

            frames = PIPELINE.wait_for_frames()
            depth_frames = ALIGN.process(frames)
            color_frame = frames.get_color_frame()
            depth_frame = depth_frames.get_depth_frame()
            
            if not color_frame: continue
        
            # RGB 프레임을 이미지로 변환
            color_image = np.asanyarray(color_frame.get_data())
            depth_iamge = np.asanyarray(depth_frame.get_data())
            
            #가이드 라인 체크
            frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.bitwise_and(frame, FACE_GUIDELINE)
            
            if not INFace(depth_frame, results):
                STR.guide = "가이드라인 안에 들어와주세요"
                return False
            
            frame = cv2.flip(frame,1)
            frame = GuideText(frame)
            cv2.imshow("", frame)


            ctime = cv2.getTickCount()  # 현재 시간 기록
            etime = (ctime - stime) / cv2.getTickFrequency()  # 경과 시간 계산


            # 5초가 경과하면 녹화 종료
            if 1 < etime < 2:
                STR.guide = '촬영을 시작합니다 2'
            elif 2 < etime < 3:
                STR.guide = '촬영을 시작합니다 1'
                
            # 동영상에 프레임을 추가
            elif etime > 3:
                STR.guide = "촬영중입니다. 움직이지마세요."
                FACEVIDEO_COLOR_WRITER.write(cv2.flip(color_image,1))
                #VIDEO_DEPTH_WRITER.write(cv2.flip(depth_iamge,1))
            if etime > 7:
                break

        # 동영상 저장 종료
        FACEVIDEO_COLOR_WRITER.release()
        #VIDEO_DEPTH_WRITER.release()

        print('동영상 저장 완료')
        
    return True
