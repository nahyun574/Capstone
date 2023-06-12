#필요한 라이브러리
import cv2
import tkinter
from PIL import Image, ImageTk
import numpy as np
import time
import mediapipe as mp
import pyrealsense2 as rs
from dataclasses import dataclass
from pathlib import Path

#생성한 라이브러리

#전역 변수설정
GUIDELINE = cv2.imread('F:/backup/Project/CapStone/code/Demo/GuideLine.png')
WIDTH = 640
HEIGHT = 480
COUNTOUT = 60

@dataclass
class Pos:
    x: float = None
    y: float = None
    z: float = None

L_SHOULDER = Pos()
R_SHOULDER = Pos()
L_EAR = Pos()
R_EAR = Pos()
NOSE = Pos()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose