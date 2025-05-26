# project_cnn_diffusion

진행할 것들

##cnn

모델 학습 진행 완료, 예측 마스크에서 성능 문제 존재

- 데이터셋 다시 확인 (1920 * 1200)
- 흰색 차선 강조 이미지 전처리

##diffusion

- 마스크 변환한 값으로 inpainting
- cnn 예측 segmentation과 and 연산한 mask로 inpainting
- 두개 값 비교
