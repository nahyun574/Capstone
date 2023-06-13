################################ 라이브러리 설정 ################################
#-*- coding: utf-8 -*-
import cv2
import tkinter
from PIL import Image, ImageTk
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import time
import mediapipe as mp
import pyrealsense2 as rs
from dataclasses import dataclass
from pathlib import Path

# 생성한 라이브러리
# from Library import *
# from guideline import *
# from save_media import *


################################ 전역 변수 설정 ################################
GUIDELINE = cv2.imread('E:/backup/Project/CapStone/code/Demo/image/GuideLine.png')
WIDTH = 640
HEIGHT = 480
COUNTOUT = 60
N_SECONDS = 2

#카메라 설정 부분
PIPELINE = rs.pipeline()
CONFIG = rs.config()
CONFIG.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)    #컬러
CONFIG.enable_stream(rs.stream.depth, WIDTH, HEIGHT, rs.format.z16, 30)     #깊이
ALIGN_TO = rs.stream.depth
ALIGN = rs.align(ALIGN_TO)

#컬러
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

#폰트 로드
FONTPATH = 'F:/backup/Project/CapStone/code/Demo/NanumGothicBold.ttf'
FONT = ImageFont.truetype(FONTPATH,20)

@dataclass
class Str:
    guide:str = " "

class Pos:
    x: float = None
    y: float = None
    z: float = None

L_SHOULDER = Pos()
R_SHOULDER = Pos()
L_EAR = Pos()
R_EAR = Pos()
NOSE = Pos()
STR = Str()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose