import streamlit as st
import os
import numpy as np
from PIL import Image

import tensorflow as tf

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# 저장 경로 설정
SAVE_DIR = "upload"
os.makedirs(SAVE_DIR, exist_ok=True)  # 해당폴더가 있는경우 오류발생 억제

st.title("구름 이미지 분류")
st.write("하늘 이미지를 업로드하면, 날씨를 예측해 드립니다.")

uploaded_file = st.file_uploader("하늘 이미지 파일을 업로드하세요.", type=["jpg", "png", "jpeg"])
print(type(uploaded_file))

if uploaded_file is not None:
    st.write("파일 이름:", uploaded_file.name)
    st.write("파일 타입:", uploaded_file.type)
    st.write("파일 크기:", uploaded_file.size, "bytes")

    st.image(uploaded_file, caption="업로드 이미지")

    # 모델 로드 및 예측
    filepath = 'best_cloud_mobilenet.keras'
    model = load_model(filepath)
    print(model)

    class_names = [
        'Ac',
        'As',
        'Cb',
        'Cc',
        'Ci',
        'Cs',
        'Ct',
        'Cu',
        'Ns',
        'Sc',
        'St'
    ]

    IMAGE_SIZE = 224

    # 이미지 준비
    image = Image.open(uploaded_file) # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1500x1500 at 0x198B95F8250>
    image_np = np.array(image)

    # cv2 대신 tf.image.resize 사용
    resized_image = tf.image.resize(image_np, (IMAGE_SIZE, IMAGE_SIZE))
    print('resized_image', type(resized_image), resized_image.shape) # <class 'tensorflow.python.framework.ops.EagerTensor'>  (224, 224, 3)
    # EagerTensor 타입을 NumPy 배열로 다시 변환
    a_image = np.array(resized_image)

    # MobileNetV2 전용 스케일링
    a_image = preprocess_input(a_image)
    batch_image = a_image.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3)
    pred_proba = model.predict(batch_image)

    pred = np.argmax(pred_proba)
    pred_label = class_names[pred]
    st.success(f"위 사진은 {pred_label} 일 확률이 {pred_proba[0][pred]:.4f} 입니다. 특징은 ........입니다.")

    # 서버에 저장
    save_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"이미지가 저장되었습니다: {save_path}")