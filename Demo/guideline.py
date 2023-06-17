from Library import *

#* 파라미터 : 미디어파이프의 랜드마크, 깊이정보 프레임
#* 반환값 : 문자열
#* 가이드라인의 좌표를 지정:
#* 어깨 : x 148,496 | y 256,480
#* 귀 : x 256,374 | y 109,183


##############어깨##############

#어깨 깊이
def Shoulder_Depth():
    #두 어깨의 깊이 차이가 0.1 이상일 때 => 카메라와 평행으로 서주세요
    if(abs(L_SHOULDER.z - R_SHOULDER.z) > 0.1):
        STR.guide = '카메라와 평행으로 서주세요'
        
    #*아닐 떄 출력
    else:
        print("왼쪽 어깨 깊이 : ({}, {}) : {} 미터".format(L_SHOULDER.x, L_SHOULDER.y, L_SHOULDER.z))
        print("오른쪽 어깨 깊이 : ({}, {}) : {} 미터".format(R_SHOULDER.x, R_SHOULDER.y, R_SHOULDER.z))
    
    #코의 좌표와 어깨 중앙의 좌표를 기준으로 
    Middle_dist = (L_SHOULDER.z + R_SHOULDER.z) / 2
    if(abs(NOSE.z - Middle_dist) > 0.1):
        STR.guide = '허리를 펴주세요'
    else:
        print('코의 깊이 : ({}, {}) : {} 미터'.format(NOSE.x, NOSE.y, NOSE.z))

#어깨 가이드라인
def INguideline(Depth,Landmarks):
    try :
        #어깨 좌표가 이미지 안에 들어와있는지 확인 및 좌표 가져오기
        L_SHOULDER.x, L_SHOULDER.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * HEIGHT
        R_SHOULDER.x, R_SHOULDER.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * HEIGHT
        L_EAR.x, L_EAR.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].y * HEIGHT
        R_EAR.x, R_EAR.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].y * HEIGHT
        NOSE.x, NOSE.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * HEIGHT
        
        L_SHOULDER.z = Depth.get_distance(int(L_SHOULDER.x), int(L_SHOULDER.y))
        R_SHOULDER.z = Depth.get_distance(int(R_SHOULDER.x), int(R_SHOULDER.y))
        NOSE.z = Depth.get_distance(int(NOSE.x), int(NOSE.y))

        
        #가이드라인 안에 있는지 확인
        if(320 < L_SHOULDER.x < 501 and 225 < L_SHOULDER.y < 480 and 137 < R_SHOULDER.x < 320 and 225 < R_SHOULDER.y < 480):
            if(254 < L_EAR.x < 387 and 82 < L_EAR.y < 225 and 254 < R_EAR.x < 387 and 82 < R_EAR.y < 225): #가이드라인 안에서
                #측정 시작부분
                return True
        
        else:
            #가이드라인 안에 들어와주세요
            STR.guide = "가이드라인 안에 들어와주세요"
        
        Shoulder_Depth()
        
    #좌표를 가져오지 못함
    except:
        #카메라 안에 들어와주세요
        STR.guide = '카메라안으로 들어와주세요'
    
    return False


##############얼굴###############

#얼굴 어깨 수직선
def INFace_shoulder(Depth,Landmarks):
    try :
        #어깨 좌표가 이미지 안에 들어와있는지 확인 및 좌표 가져오기
        L_SHOULDER.x, L_SHOULDER.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * HEIGHT
        R_SHOULDER.x, R_SHOULDER.y = Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * WIDTH, Landmarks.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * HEIGHT
    except:
        #카메라 안에 들어와주세요
        STR.guide = '카메라안으로 들어와주세요'
    
    return False

#얼굴 가이드라인
def INFace(Depth,Landmarks):
    try :
        face_landmarks = Landmarks.multi_face_landmarks[0] 
        chin_landmark = face_landmarks.landmark[152]
        chin_x = int(chin_landmark.x * 640)
        chin_y = int(chin_landmark.y * 480)
            
        forhead_landmark = face_landmarks.landmark[10]
        forhead_x = int(forhead_landmark.x * 640)
        forhead_y = int(forhead_landmark.y * 480)
    
        if(280 < chin_x < 340 and  400 < chin_y < 420 and 300 < forhead_x < 400 and 53 < forhead_y < 133):
            print(f"chin 좌표: ({chin_x}, {chin_y})")
            print(f"forhead 좌표: ({forhead_x}, {forhead_y})")
            #측정 시작부분
            return True
        
        else:
            #가이드라인 안에 들어와주세요
            STR.guide = "가이드라인 안에 들어와주세요"
    
    #좌표를 가져오지 못함
    except:
        #카메라 안에 들어와주세요
        STR.guide = '카메라안으로 들어와주세요'
    
    return False
    
