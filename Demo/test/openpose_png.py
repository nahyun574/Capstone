import cv2
import numpy as np
from pathlib import Path

# MPII에서 각 파트 번호, 선으로 연결될 POSE_PAIRS
BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13,
              "Background": 15}

POSE_PAIRS = [["Neck", "RShoulder"], ["RShoulder", "RElbow"],
              ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
              ["LElbow", "LWrist"], ["RHip", "RKnee"],
              ["RKnee", "RAnkle"], ["LHip", "LKnee"], ["LKnee", "LAnkle"]]

# 각 파일 path
BASE_DIR = Path("__file__").resolve().parent
protoFile = str(BASE_DIR) + "/Demo/pose_deploy_linevec.prototxt"
weightsFile = str(BASE_DIR) + "/Demo/pose_iter_160000.caffemodel"

# 위의 path에 있는 network 모델 불러오기
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# PNG 이미지 파일 경로
image_path = 'F:/backup/Project/CapStone/code/Demo/test/2.png'

# 이미지 파일 로드
frame = cv2.imread(image_path)

frameWidth = frame.shape[1]
frameHeight = frame.shape[0]

inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (368, 368), (127.5, 127.5, 127.5), swapRB=True, crop=False)

net.setInput(inpBlob)

output = net.forward()

points = []
for i in range(0, 15):
    probMap = output[0, i, :, :]

    minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

    x = (frameWidth * point[0]) / output.shape[3]
    y = (frameHeight * point[1]) / output.shape[2]

    if prob > 0.1:
        cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
        cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                    lineType=cv2.LINE_AA)
        points.append((int(x), int(y)))
    else:
        points.append(None)

for pair in POSE_PAIRS:
    partA = pair[0]
    partA = BODY_PARTS[partA]
    partB = pair[1]
    partB = BODY_PARTS[partB]

    if points[partA] and points[partB]:
        cv2.line(frame, points[partA], points[partB], (0, 255, 0), 2)

cv2.imshow("Output-Keypoints", frame)
cv2.imwrite(image_path[:-5] + 'openpose.png',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
