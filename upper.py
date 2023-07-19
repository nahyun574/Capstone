from Library import *

#골반 깊이
def Pelvis_Depth():
    #두 골반의 깊이 차이가 0.1 이상일 때 => 카메라와 평행으로 서주세요
    if(abs(L_PEL.z - R_PEL.z) > 70):
        STR.guide = '카메라와 평행으로 서주세요'
                
    #*아닐 떄 출력
    #else:
        
    #무릎의 좌표와 골반 중앙의 좌표를 기준으로 
    Middle_dist_p = (L_PEL.z + R_PEL.z) / 2
    Middle_dist_k = (L_KNEE.z + L_KNEE.z) / 2
    if(abs(Middle_dist_k - Middle_dist_p) > 70):
        STR.guide = '무릎을 펴주세요'
    
    #짝다리 판별
    Middle_dist_px = (L_PEL.x + R_PEL.x / 2)
    if(abs(abs(Middle_dist_px - L_FOOT.x) - abs(Middle_dist_px - R_FOOT.x)) > 10):
        STR.guide = '발의 위치를 동일하게 해주세요'

#골반 가이드라인
def INPelvis_guideline(Depth,Landmarks):
    try :
        #골반 좌표가 이미지 안에 들어와있는지 확인 및 좌표 가져오기
        L_PEL.x, L_PEL.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * HEIGHT
        R_PEL.x, R_PEL.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * HEIGHT
        L_KNEE.x, L_KNEE.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y * HEIGHT
        R_KNEE.x, R_KNEE.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y * HEIGHT
        L_FOOT.x, L_FOOT.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y * HEIGHT
        R_FOOT.x, R_FOOT.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y * HEIGHT

        
        if 0 <= int(L_PEL.x) < WIDTH and 0 <= int(L_PEL.y) < HEIGHT:
            if 0 <= int(R_PEL.x) < WIDTH and 0 <= int(R_PEL.y) < HEIGHT:
                if 0 <= int(L_KNEE.x) < WIDTH and 0 <= int(L_KNEE.y) < HEIGHT:
                    if 0 <= int(L_KNEE.x) < WIDTH and 0 <= int(L_KNEE.y) < HEIGHT:
                        L_PEL.z = Depth.get_distance(int(L_PEL.x), int(L_PEL.y))
                        R_PEL.z = Depth.get_distance(int(R_PEL.x), int(R_PEL.y))
                        L_KNEE.z = Depth.get_distance(int(L_KNEE.x), int(L_KNEE.y))
                        R_KNEE.z = Depth.get_distance(int(R_KNEE.x), int(R_KNEE.y))

        
        #가이드라인 안에 있는지 확인
        if(0 < L_PEL.x < 272 and 0 < L_PEL.y < 460 and 0 < R_PEL.x < 272 and 0 < R_PEL.y < 460):
            if(0 < L_KNEE.x < 272 and 0 < L_KNEE.y < 460 and 0 < R_KNEE.x < 272 and 0 < R_KNEE.y < 460): #가이드라인 안에서
                #측정 시작부분
                return True
        
        else:
            #가이드라인 안에 들어와주세요
            STR.guide = "가이드라인 안에 들어와주세요"
        
        Pelvis_Depth()
        
    #좌표를 가져오지 못함
    except:
        #카메라 안에 들어와주세요
        STR.guide = '카메라안으로 들어와주세요'
    
    return False

def GuideText(frame):
    #텍스트 위치 계산
    text_x, text_y = int((HEIGHT - len(STR.guide)*7) / 2), 40 #가로 중앙으로 설정

    frame = Image.fromarray(frame)
    ImageDraw.Draw(frame).text((text_x,text_y), STR.guide, font=FONT, fill=GREEN)

    frame = np.array(frame)
    return frame


##############골반 비디오##############

"""def Pelvis_video(cam_label):
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
            Pelvis_video(cam_label)"""

#골반 가이드라인 겹치기
def Media_Pelvis():
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
            if 0 <= int(L_PEL.x) < WIDTH and 0 <= int(L_PEL.y) < HEIGHT:
                if 0 <= int(R_PEL.x) < WIDTH and 0 <= int(R_PEL.y) < HEIGHT:
                    L_PEL.z = depth.get_distance(int(L_PEL.x), int(L_PEL.y))
                    R_PEL.z = depth.get_distance(int(R_PEL.x), int(R_PEL.y))
                    MIDDLE_PEL.z = (L_PEL.z + R_PEL.z) / 2
                    
            if 0 <= int(L_KNEE.x) < WIDTH and 0 <= int(L_KNEE.y) < HEIGHT:
                if 0 <= int(R_KNEE.x) < WIDTH and 0 <= int(R_KNEE.y) < HEIGHT:
                    L_KNEE.z = depth.get_distance(int(L_KNEE.x), int(L_KNEE.y))
                    R_KNEE.z = depth.get_distance(int(R_KNEE.x), int(R_KNEE.y))
                    MIDDLE_KNEE.z = (L_KNEE.z + R_KNEE.z) / 2
            

            # #가이드라인 확인 5초마다
            if time.time() - Start_Time > N_SECONDS:
                count += 1
                Start_Time = time.time()

                if INPelvis_guideline(depth, MP_landmark):
                    saveon = Pelvis_save()

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
            #frame = cv2.bitwise_and(frame,GUIDELINE)
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

#골반 영상 저장
def Pelvis_save():
    VIDEO_COLOR_WRITER = cv2.VideoWriter(ROOT_DIR + '/image/pelvis_color_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (WIDTH, HEIGHT), isColor = True)
    #VIDEO_DEPTH_WRITER = cv2.VideoWriter('C:/lab/Demo/image/depth_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (WIDTH, HEIGHT), isColor = True)
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
            #frame = cv2.bitwise_and(frame, GUIDELINE)
            
            if not INPelvis_guideline(depth_frame, results):
                STR.guide = "카메라 안에 들어와주세요"
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
            if etime > 8:
                break

        # 동영상 저장 종료
        VIDEO_COLOR_WRITER.release()

        print('동영상 저장 완료')
        
    return True

#############골반 측정###############

def Pelvis_incline(lx, ly, rx, ry):
    #깊이, 2.5 = MIDDLE_PEL.z
    PEL_DIS.x = (870 / ((1/6) * 2.5 *1000))  * (ry-ly)
    
    # 0 : 평행
    # -1 : 오류
    # 2 : 왼쪽이 높음
    # 3 : 오른쪽이 높음
    if 0 <= (PEL_DIS.x) <= 10: 
        #R_TEXT.guide = '균형'
        print("균형")
    elif lx - rx == 0:
        #R_TEXT.guide = '인식불가'
        print("인식불가")
    else:
        if (ry-ly) / (rx-lx) > 0:
            if abs(PEL_DIS.x) > 20:
                #R_TEXT.guide = '왼쪽어깨'
                #R_TY_TEXT.guide = '고도 비대칭'
                print('왼쪽골반')
                print('고도 비대칭')
            elif abs(PEL_DIS.x) > 15:
                #R_TEXT.guide = '왼쪽어깨'
                #R_TY_TEXT.guide = '중도 비대칭'
                print('왼쪽골반')
                print('중도 비대칭')
            else:
                #R_TEXT.guide = '왼쪽어깨'
                #R_TY_TEXT.guide = '경도 비대칭'
                print('왼쪽골반')
                print('경도비대칭')
            
        else:
            if abs(PEL_DIS.x) > 20:
                #R_TEXT.guide = '오른쪽어깨'
                #R_TY_TEXT.guide = '고도 비대칭'
                print('오른쪽골반')
                print('고도 비대칭') 
            elif abs(PEL_DIS.x) > 15:
                #R_TEXT.guide = '오른쪽어깨'
                #R_TY_TEXT.guide = '중도 비대칭'
                print('오른쪽골반')
                print('고도 비대칭') 
            else:
                #R_TEXT.guide = '오른쪽어깨'
                #R_TY_TEXT.guide = '경도 비대칭'
                print('오른쪽골반')
                print('고도 비대칭')

#골반 스코어링
def Pelvis_score():
    if abs(PEL_DIS.x) < 1:
        P_SCORE.guide, P_SCORE_I.guide = 100, 100
    elif abs(PEL_DIS.x) < 2:
        P_SCORE.guide, P_SCORE_I.guide = 99, 99
    elif abs(PEL_DIS.x) <= 10:
        P_SCORE.guide, P_SCORE_I.guide = (100 - int(abs(PEL_DIS.x) * 1)), (100 - int(abs(PEL_DIS.x) * 1))
    elif 10 < abs(PEL_DIS.x) < 100:
        P_SCORE.guide, P_SCORE_I.guide = (110 - int(abs(PEL_DIS.x) * 2)), (110 - int(abs(PEL_DIS.x) * 2))
    else:
        P_SCORE.guide = "잘못 측정"

#골반 결과 측정
def Pelvis(Landmarks):
    L_PEL.x, L_PEL.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * HEIGHT
    R_PEL.x, R_PEL.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * HEIGHT
    
    SUM_LS.x += L_PEL.x
    SUM_LS.y += L_PEL.y
    SUM_RS.x += R_PEL.x
    SUM_RS.y += R_PEL.y
    
def Sum_Pelvis(i):
    SUM_LPEL.x = SUM_LPEL.x / float(i-1)
    SUM_LPEL.y = SUM_LPEL.y / float(i-1)
    SUM_RPEL.x = SUM_RPEL.x / float(i-1)
    SUM_RPEL.y = SUM_RPEL.y / float(i-1) 
                
    Pelvis_incline(SUM_LPEL.x, SUM_LPEL.y, SUM_RPEL.x, SUM_RPEL.y)
                
def Pelvis_Video_result():   
    # 동영상 파일 경로
    video_path = 'C:/lab/Demo/image/pelvis_color_output.mp4'

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
                    
                    Pelvis(MP_landmark)
                        
                    mp_drawing.draw_landmarks(
                        frame,
                        MP_landmark.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                    
                    cv2.imshow('Output', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            except:
                Sum_Pelvis(i)
                Pelvis_score()
                
                cv2.destroyAllWindows()
                break

        cap.release()

PIPELINE.start(CONFIG)
Media_Pelvis()
cv2.destroyAllWindows()
PIPELINE.stop()

Pelvis_Video_result()