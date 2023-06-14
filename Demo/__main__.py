from Library import *
from media import *


class Program(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self) # 페이지 생성
        self._frame = None
        self.switch_frame(Main_Page)
        window_width = 920 # 너비
        window_height = 640 # 높이
        window_pos_x = 500 # 초기 x좌표
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
        button_shoulder = tkinter.Button(self,text ="어깨 불균형 측정",command=lambda: (master.switch_frame(Shoulder_Page))).pack()

        #button_close = tkinter.Button(self,text="종료하기", command=quit()).pack()

# 얼굴 불균형 측정 화면
class Face_Page(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)

        tkinter.Label(self,text="얼굴측정").pack(side="top") #,fill="x",pady=5)

        self.cam_frame_face = tkinter.Frame(self, bg="white", width=640, height=480) #영상나올 프레임
        self.cam_frame_face.pack(side="top")
        self.cam_label = tkinter.Label(self.cam_frame_face)
        self.cam_label.grid()
        button_main = tkinter.Button(self, text="메인 화면으로",command=lambda: (master.switch_frame(Main_Page),PIPELINE.stop())).pack(side="bottom")

        PIPELINE.start(CONFIG)
        time.sleep(1)
        worker = threading.Thread(target=video(self.cam_label))
        worker.daemon = True
        worker.start()
        
# 어깨 불균형 측정 화면
class Shoulder_Page(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)
        tkinter.Label(self,text="어깨측정").pack(side="top") #,fill="x",pady=5)
        
        PIPELINE.start(CONFIG)
        Media_Shoulder()
        cv2.destroyAllWindows()
        PIPELINE.stop()
        
        button_main = tkinter.Button(self, text="메인 화면으로",command=lambda: (master.switch_frame(Main_Page))).pack(side="bottom")

if __name__ == "__main__":
    app = Program()
    app.mainloop()
