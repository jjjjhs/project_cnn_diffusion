import os
import numpy as np
import cv2
from PIL import Image, ImageOps
from tqdm import tqdm

seg_viz_folder      = "C:/Users/jhs38/Desktop/viz_prediction"
inpaint_mask_folder = "C:/Users/jhs38/Desktop/1920_1080_inpainting_mask"
input_folder        = "C:/Users/jhs38/Desktop/viz_origin"
output_folder       = "C:/Users/jhs38/Desktop/viz_origin_masked"
os.makedirs(output_folder, exist_ok=True)

w, h      = 30, 30
num_masks = 10

for img_fn in tqdm(sorted(os.listdir(input_folder)), desc="마스크 생성"):
    if not img_fn.lower().endswith(".png"):
        continue

    name = os.path.splitext(img_fn)[0]            # ex. '15153240_origin'
    # '_origin' 제거
    core = name[:-len("_origin")] if name.endswith("_origin") else name
    # seg/file names
    seg_fn       = f"{core}_pred.png"            # ex. '15153240_pred.png'
    inpaint_fn   = f"{core}_mask.png"            # ex. '15153240_mask.png'

    img_path     = os.path.join(input_folder, img_fn)
    seg_path     = os.path.join(seg_viz_folder, seg_fn)
    inpaint_path = os.path.join(inpaint_mask_folder, inpaint_fn)
    out_path     = os.path.join(output_folder, img_fn)

    # 파일 유효성 체크
    if not os.path.exists(seg_path):
        print(f"[SKIP] seg 파일 없음: {seg_path}")
        continue
    if not os.path.exists(inpaint_path):
        print(f"[SKIP] inpaint mask 없음: {inpaint_path}")
        continue

    # 로드 & 리사이징
    img    = cv2.imread(img_path)
    seg    = cv2.imread(seg_path, cv2.IMREAD_GRAYSCALE)
    mask   = cv2.imread(inpaint_path, cv2.IMREAD_GRAYSCALE)
    img    = cv2.resize(img, (960, 540))
    seg    = cv2.resize(seg, (960, 540))
    mask   = cv2.resize(mask, (960, 540))

    # 차선 픽셀만 가져오기
    ys, xs = np.where(seg > 127)
    if len(ys) < num_masks:
        print(f"[WARN] 충분한 차선 픽셀 없음: {core}")
        continue

    # 랜덤으로 num_masks만큼 박스 그리기
    for _ in range(num_masks):
        idx = np.random.randint(len(ys))
        y_c, x_c = ys[idx], xs[idx]
        x1 = max(0, x_c - w//2)
        y1 = max(0, y_c - h//2)
        x2 = min(960, x1 + w)
        y2 = min(540, y1 + h)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,0), -1)

    cv2.imwrite(out_path, img)
    print(f"[SAVE] {out_path}")

print("✅ 차선 위주 마스크 생성 완료")
