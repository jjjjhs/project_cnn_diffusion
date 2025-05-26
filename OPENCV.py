import cv2
import os
import numpy as np
import random

# 폴더 경로 설정
input_dir = 'images_original/'
output_img_dir = 'images_masked/'
output_mask_dir = 'masks/'
skipped_dir = 'skipped/'

# 폴더 생성
os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_mask_dir, exist_ok=True)
os.makedirs(skipped_dir, exist_ok=True)

def create_masked_and_mask(img_path, save_name):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (640, 360))

    # ========== [1] 흰색 차선 마스크 생성 ==========
    lower_white = np.array([200, 200, 200])
    upper_white = np.array([255, 255, 255])
    mask = cv2.inRange(img, lower_white, upper_white)
    binary_mask = (mask // 255).astype(np.uint8)

    # ========== [2] 차선이 없다면 skipped 폴더에 저장 ==========
    if np.sum(binary_mask) == 0:
        skipped_path = os.path.join(skipped_dir, save_name)
        cv2.imwrite(skipped_path, img)
        print(f"⏭️ {save_name} → 차선 없음 → skipped/에 저장됨")
        return

    # ========== [3] 손상 이미지 만들기 ==========
    masked = img.copy()
    for _ in range(2):
        x = random.randint(220, 420)
        y = random.randint(200, 300)
        w, h = random.choice([(100, 30), (100, 10), (50, 50)])
        cv2.rectangle(masked, (x, y), (x + w, y + h), (0, 0, 0), -1)

    # ========== [4] 이미지 & 마스크 저장 ==========
    cv2.imwrite(os.path.join(output_img_dir, save_name), masked)
    cv2.imwrite(os.path.join(output_mask_dir, save_name.replace('.jpg', '.png')), binary_mask * 255)
    print(f"✅ {save_name} 저장 완료")

# ========== 전체 이미지 처리 ==========
for filename in os.listdir(input_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        full_path = os.path.join(input_dir, filename)
        create_masked_and_mask(full_path, filename)

print("🎉 전체 완료: 손상 이미지 + 마스크 생성, 차선 없는 건 skipped/")
