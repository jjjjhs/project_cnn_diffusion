# import os
# import random
# import numpy as np
# import cv2
# from glob import glob

# input_dir = "C:/Users/jhs38/Desktop/c_1280_720_daylight_train_f"         # 원본 이미지 폴더
# output_dir = "C:/Users/jhs38/Desktop/c_1280_720_daylight_train_masked"  # 저장할 폴더
# os.makedirs(output_dir, exist_ok=True)

# # 이미지 목록 불러오기
# image_paths = glob(os.path.join(input_dir, '*.jpg'))

# for path in image_paths:           
#     img = cv2.imread(path)
#     img = cv2.resize(img, (640, 360))
    
#     # 마스킹 적용
#     masked = img.copy()
#     w, h = 30, 30  # 마스킹 박스 크기

#     # 저장
#     filename = os.path.basename(path)
#     cv2.imwrite(os.path.join(output_dir, filename), masked)

import os
import random
import numpy as np
import cv2
from glob import glob

input_dir = "C:/Users/jhs38/Desktop/c_1280_720_daylight_train_f"         # 원본 이미지 폴더
output_dir = "C:/Users/jhs38/Desktop/c_1280_720_daylight_train_masked2"  # 저장할 폴더
os.makedirs(output_dir, exist_ok=True)

# 이미지 목록 불러오기
image_paths = glob(os.path.join(input_dir, '*.jpg'))

for path in image_paths:           
    img = cv2.imread(path)
    img = cv2.resize(img, (640, 360))

    masked = img.copy()
    w, h = 30, 30  # 마스킹 박스 크기
    num_masks = 10  # 마스킹할 박스 개수

    for _ in range(num_masks):
        # 적당히 퍼트리기 위해 전체 영역에서 랜덤하게
        #x = random.randint(0, 640 - w)
        #y = random.randint(0, 360 - h)
        #cv2.rectangle(masked, (x, y), (x + w, y + h), (0, 0, 0), -1)
        # x좌표는 중앙 근처 (220~420)
        x = random.randint(60, 580) 
        y_center = random.randint(140, 220)
        y = y_center - h // 2  # h = 30
        cv2.rectangle(masked, (x, y), (x + w, y + h), (0, 0, 0), -1)


    # 저장
    filename = os.path.basename(path)
    cv2.imwrite(os.path.join(output_dir, filename), masked)
