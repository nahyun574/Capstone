from Library import *

#* 파라미터 : 미디어파이프의 랜드마크, 깊이정보 프레임
#* 반환값 : 문자열
#* 가이드라인의 좌표를 지정:
#* 어깨 : x 148,496 | y 256,480
#* 귀 : x 256,374 | y 109,183

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
        if(148 < L_SHOULDER.x < 496 and 265 < L_SHOULDER.y < 480 and 148 < R_SHOULDER.x < 496 and 265 < R_SHOULDER.y < 480):
            if(258 < L_EAR.x < 374 and 109 < L_EAR.y < 183 and 258 < R_EAR.x < 374 and 109 < R_EAR.y < 183): #가이드라인 안에서
                print("왼쪽 어깨 : ", L_SHOULDER.x, L_SHOULDER.y)
                print("오른쪽 어깨 : ", R_SHOULDER.x, R_SHOULDER.y)
                return True
        
        else:
            #가이드라인 안에 들어와주세요
            print("가이드라인 안에 들어와주세요")
            return False
        
        #depth()
        
    #좌표를 가져오지 못함
    except:
        #카메라 안에 들어와주세요
        print('카메라안으로 들어와주세요')
        return False
        
#*아직은 출력만
def depth():
    #두 어깨의 깊이 차이가 0.1 이상일 때
    if(abs(L_SHOULDER.z - R_SHOULDER.z) > 0.1):
        print('어깨 깊이 차이 > 0.1')
        
    #아닐 떄 출력
    else:
        print("왼쪽 어깨 깊이 : ({}, {}) : {} 미터".format(L_SHOULDER.x, L_SHOULDER.y, L_SHOULDER.z))
        print("오른쪽 어깨 깊이 : ({}, {}) : {} 미터".format(R_SHOULDER.x, R_SHOULDER.y, R_SHOULDER.z))
    
    #코의 좌표와 어깨 중앙의 좌표를 기준으로 
    Middle_dist = (L_SHOULDER.z + R_SHOULDER.z) / 2
    if(abs(NOSE.z - Middle_dist) > 0.2):
        print('허리를 펴주세요')
    else:
        print('코의 깊이 : ({}, {}) : {} 미터'.format(NOSE.x, NOSE.y, NOSE.z))
        
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

# def Shoulder(image,results):
#         if(148 < L_SHOULDER.x < 496 and 265 < L_SHOULDER.y < 480 and 148 < R_SHOULDER.x < 496 and 265 < R_SHOULDER.y < 480):
#             if(258 < L_EAR.x < 374 and 109 < L_EAR.y < 183 and 258 < R_EAR.x < 374 and 109 < R_EAR.y < 183): #가이드라인 안에서
#                 print("left _SHOULDER : ", L_SHOULDER.x, L_SHOULDER.y)
                
#                 lsx_li.append(L_SHOULDER.x)
#                 lsy_li.append(L_SHOULDER.y)

#                 print("right _SHOULDER : ", R_SHOULDER.x, R_SHOULDER.y)
                
#                 rsx_li.append(R_SHOULDER.x)
#                 rsy_li.append(R_SHOULDER.y)

#                 if(len(rsy_li) == 5):
#                     Ls.x = sum(lsx_li) / 5
#                     Ls.y = sum(lsy_li) / 5
#                     Rs.x = sum(rsx_li) / 5
#                     Rs.y = sum(rsy_li) / 5 #5번 찍고 평균
                    
#                     _SHOULDER_result(Ls.x, Ls.y, Rs.x, Rs.y)
                    
#                     lsx_li.clear()
#                     lsy_li.clear()
#                     rsx_li.clear()
#                     rsy_li.clear() #초기화

#             else:
#                 print("가이드라인 안에 들어와주세요")
#         else:
#             print("가이드라인 안에 들어와주세요")

#     else:
#         print("카메라 앞에 바르게 서주세요")
#         #값 안들어오면 메세지

# def _SHOULDER_result(lx, ly, rx, ry):
#     incline = _SHOULDER_incline(lx, ly, rx, ry)
    
#     if incline == 0 : print('균형')
#     elif incline == -1: print('인식 불가')
#     elif incline == 2 : print('왼쪽어깨')
#     else: print("오른쪽 어깨")   