from Library import *
from media import *
from result import *


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
        button_face = tkinter.Button(self, text="얼굴 불균형 측정", command=lambda: master.switch_frame(Face_Page)).pack()
        button_shoulder = tkinter.Button(self, text ="어깨 불균형 측정", command=lambda: (master.switch_frame(Shoulder_Page))).pack()
        button_face_result = tkinter.Button(self, text="얼굴결과보기",command=lambda: (master.switch_frame(Face_result))).pack()
        button_shoulder_result = tkinter.Button(self, text="어깨결과보기",command=lambda: (master.switch_frame(Shoulder_result))).pack(side="bottom")
        #button_close = tkinter.Button(self,text="종료하기", command=quit()).pack()

# 얼굴 불균형 측정 화면
class Face_Page(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)

        tkinter.Label(self,text="얼굴측정").pack(side="top") #,fill="x",pady=5)

        PIPELINE.start(CONFIG)
        Media_Face()
        cv2.destroyAllWindows()
        PIPELINE.stop()
        
        button_face_result = tkinter.Button(self, text="결과보기",command=lambda: (master.switch_frame(Face_result))).pack(side="bottom")
        button_main = tkinter.Button(self, text="메인 화면으로",command=lambda: (master.switch_frame(Main_Page))).pack(side="bottom")

#얼굴 결과보기 화면
class Face_result(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)
        tkinter.Label(self,text="얼굴결과").pack(side="top") #,fill="x",pady=5)
        
        Face_Video_result()
        
        if(FC_LR_TEXT.guide != '대칭' or FC_CENTER_TEXT.guide != '대칭'):
            label_text_F_TEXT = f"얼굴비대칭: {F_TEXT.guide}"  # 텍스트 문자열 생성
        label_text_FA_TEXT = f"눈과 입의 각도: {FA_TEXT.guide}"
        label_text_FC_LR_TEXT = f"좌우 안면비대칭: {FC_LR_TEXT.guide}"
        label_text_FC_CENTER_TEXT = f"중앙 안면비대칭: {FC_CENTER_TEXT.guide}"
        label = tkinter.Label(self, text=label_text_F_TEXT)  # 라벨 생성 및 텍스트 설정
        label.pack()
        label_ty = tkinter.Label(self, text=label_text_FA_TEXT)
        label_ty.pack()
        label_ty = tkinter.Label(self, text=label_text_FC_LR_TEXT)
        label_ty.pack()
        label_ty = tkinter.Label(self, text=label_text_FC_CENTER_TEXT)
        label_ty.pack()
        
        button_main = tkinter.Button(self, text="메인 화면으로",command=lambda: (master.switch_frame(Main_Page))).pack(side="bottom")
        
# 어깨 불균형 측정 화면
class Shoulder_Page(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)
        tkinter.Label(self,text="어깨측정").pack(side="top") #,fill="x",pady=5)
        
        PIPELINE.start(CONFIG)
        Media_Shoulder()
        cv2.destroyAllWindows()
        PIPELINE.stop()
        
        button_shoulder_result = tkinter.Button(self, text="결과보기",command=lambda: (master.switch_frame(Shoulder_result))).pack(side="bottom")
        button_main = tkinter.Button(self, text="메인 화면으로",command=lambda: (master.switch_frame(Main_Page))).pack(side="bottom")

#어깨 결과보기 화면
class Shoulder_result(tkinter.Frame):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master)
        tkinter.Label(self,text="어깨결과").pack(side="top") #,fill="x",pady=5)
        
        Video_result()
        
        label_text_R_TEXT = f"어깨비대칭: {R_TEXT.guide}"  # 텍스트 문자열 생성
        label_text_R_TY = f"어깨척도: {R_TY_TEXT.guide}"
        label = tkinter.Label(self, text=label_text_R_TEXT)  # 라벨 생성 및 텍스트 설정
        label.pack()
        label_ty = tkinter.Label(self, text=label_text_R_TY)
        label_ty.pack()
        
        button_main = tkinter.Button(self, text="메인 화면으로",command=lambda: (master.switch_frame(Main_Page))).pack(side="bottom")


if __name__ == "__main__":
    app = Program()
    app.mainloop()
