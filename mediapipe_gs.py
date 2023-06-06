# -*- coding: utf-8 -*-
import cv2
import PIL.Image, PIL.ImageTk
import tkinter
from PIL import Image, ImageTk
import numpy as np
import time
import show_fps
import mediapipe as mp
import pyrealsense2 as rs

Lshoulder_x = 0
Lshoulder_y = 0
Rshoulder_x = 0
Rshoulder_y = 0
lsx_li = []
lsy_li = []
rsx_li = []
rsy_li = []

#가이드라인 이미지 불러오고 GraySCale, Edge 검출
img = cv2.imread('GuideLine_v5.0.3.png')
edges = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.resize(edges,(640,480))
#edges = cv2.Canny(gray,50,150,apertureSize=3)
inputScale = 1.0/255

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
    global Lshoulder_x, Lshoulder_y, Rshoulder_x, Rshoulder_y
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

def media(cam_label):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    # For webcam input:
    #fps = cap.get(cv2.CAP_PROP_FPS) #웹 캠에서 fps값 획득
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    setWidth = 640
    setHeight = 480


    
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, setWidth, setHeight, rs.format.bgr8, 30)
    pipeline.start(config)

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        frames = pipeline.wait_for_frames()
        image = frames.get_color_frame()
        depth = frames.get_depth_frame()
        
        if not depth:
            return
        if not image:
            return
        
        if 0 <= int(Lshoulder_x) < setWidth and 0 <= int(Lshoulder_y) < setHeight:
            Ls_dist = depth.get_distance(int(Lshoulder_x), int(Lshoulder_y))
            Rs_dist = depth.get_distance(int(Rshoulder_x), int(Rshoulder_y))# 특정 픽셀에서의 깊이 값을 가져옴
                
        resize_edges = np.repeat(edges[:,:,np.newaxis],3,-1)
        image = np.asanyarray(image.get_data())
        image_height, image_width, _ = image.shape
        
        # 엣지 추가
        image = cv2.bitwise_and(image, resize_edges)
        
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        #어깨 좌표 구하는 함수
        if i == 10:
            Shoulder(image,results)
            print("Depth at pixel ({}, {}): {} meters".format(Lshoulder_x, Lshoulder_y, Ls_dist))
            print("Depth at pixel ({}, {}): {} meters".format(Rshoulder_x, Rshoulder_y, Rs_dist))
            i = 0
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        image = cv2.flip(image,1)
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        cam_label.imgtk = imgtk
        cam_label.configure(image=imgtk)
        cam_label.after(10,media(cam_label))

class Program(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self) # 페이지 생성
        self._frame = None
        self.switch_frame(Main_Page)
        window_width = 920 # 너비
        window_height = 640 # 높이
        window_pos_x = 700 # 초기 x좌표
        window_pos_y = 100 # 초기 y좌표
        self.geometry("{}x{}+{}+{}".format(window_width,window_width,window_pos_x,window_pos_y))
            
        # 생성한 창 크기 사이즈 조절 가능여부
        self.resizable(0,0)
        self.title("Tkinter_demo")
            
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
# 메인 화면
class Main_Page(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)
        
        tkinter.Label(self, text="신체 불균형 측정 프로그램").pack(side="top",fill="x",pady=5)
        button_face = tkinter.Button(self, text="얼굴 불균형 측정",command=lambda: master.switch_frame(Face_Page)).pack()
        button_shoulder = tkinter.Button(self,text ="어깨 불균형 측정",command=lambda: master.switch_frame(Shoulder_Page)).pack()

        #button_close = tkinter.Button(self,text="종료하기", command=quit()).pack()

# 얼굴 불균형 측정 화면
import cv2
class Face_Page(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)
        
        tkinter.Label(self,text="얼굴측정").pack(side="top")#,fill="x",pady=5)
        
        cam_frame_face = tkinter.Frame(self, bg="white", width=640, height=480) #영상나올 프레임
        cam_frame_face.pack(side="top")
        cam_label = tkinter.Label(cam_frame_face)
        cam_label.grid()
        
        cap = cv2.VideoCapture(1)
        def video_play():
            ret, frame = cap.read() # 프레임이 올바르게 읽히면 ret은 True
            if not ret:
                cap.release() # 작업 완료 후 해제
                return
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame,1)
            img = Image.fromarray(frame) # Image 객체로 변환
            imgtk = ImageTk.PhotoImage(image=img) # ImageTk 객체로 변환
            # OpenCV 동영상
            cam_label.imgtk = imgtk
            cam_label.configure(image=imgtk)
            cam_label.after(10, video_play)
        video_play()

        button_main = tkinter.Button(self, text="메인 화면으로",command=lambda: master.switch_frame(Main_Page)).pack(side="bottom")
        
        
# 어깨 불균형 측정 화면
class Shoulder_Page(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)
        tkinter.Label(self,text="어깨측정").pack(side="top")#,fill="x",pady=5)
        
        cam_frame_shoulder = tkinter.Frame(self, bg="white", width=640, height=480)
        cam_frame_shoulder.pack(size="top")
        cam_label = tkinter.Label(cam_frame_shoulder)
        cam_label.grid()
        
        media(cam_label)

        button_main = tkinter.Button(self, text="메인 화면으로",command=lambda: master.switch_frame(Main_Page)).pack(side="bottom")
        
if __name__ == "__main__":
    app = Program()
    app.mainloop()
