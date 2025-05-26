import cv2
import numpy as np
from PIL import Image
import os
from glob import glob


# ======================
# 1. 폴더 경로 설정
# ======================
input_folder = r"C:/Users/jhs38/Desktop/masked_images"   # <- 이미지가 있는 폴더
output_folder = r"C:/Users/jhs38/Desktop/inpainting_mask"  # output 폴더가 다르면 경로 따로 지정해도 됨

# ======================
# 2. 파일 리스트 가져오기
# ======================
# 확장자별로 처리 (JPG, JPEG, PNG 등)
img_extensions = ['*.jpg', '*.jpeg', '*.png']
img_files = []
for ext in img_extensions:
    img_files.extend(glob(os.path.join(input_folder, ext)))

print(f"총 {len(img_files)}개 파일 처리 시작!")


# ======================
# 3. 이미지별로 마스킹 처리
# ======================
for input_path in img_files:
    try:
        # 파일명에서 확장자 제거 후 _mask.png로 저장
        base = os.path.splitext(os.path.basename(input_path))[0]
        output_mask_path = os.path.join(output_folder, f"{base}_mask.png")

        # 이미지 로드
        img = cv2.imread(input_path)
        if img is None:
            print(f"이미지 파일을 찾을 수 없음: {input_path}")
            continue

        # 그레이스케일 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 임계값 처리 (threshold 값은 5~50 사이 조정)
        _, mask = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY_INV)

        # 작은 노이즈 제거
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # 저장
        cv2.imwrite(output_mask_path, mask)
        print(f"[✔] {os.path.basename(input_path)} → {os.path.basename(output_mask_path)} 저장 완료")
    except Exception as e:
        print(f"[!] {input_path} 변환 중 오류 발생: {e}")

print("=== 모든 이미지 마스킹 완료 ===")