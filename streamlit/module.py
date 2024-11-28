#----------------------------------------------#
# 필요한 module
import numpy as np
import os
from PIL import Image

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

import tensorflow as tf
print(tf.__version__)


filepath = './EfficientNet_class10_final.keras'
model = load_model(filepath)
#----------------------------------------------#
# web에 올라온 image
def upload_image(uploaded_file):

    # 저장 경로 설정
    SAVE_DIR = "upload_img"
    os.makedirs(SAVE_DIR, exist_ok=True)

    # 이미지 준비
    # uploaded_file은 UploadedFile 객체이다. # > app.py에서 선언하고 함수 호출 시에 넘겨 줘야함
    IMAGE_SIZE = 224
    image = Image.open(uploaded_file)  # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1500x1500 at 0x198B95F8250>
    image_np = np.array(image)
    # tf.image.resize 사용
    resized_image = tf.image.resize(image_np, (IMAGE_SIZE, IMAGE_SIZE))
    # Tensor를 numpy 배열로 변환
    a_image = np.array(resized_image)
    a_image = preprocess_input(a_image)

    batch_image = a_image.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3)

    # 서버에 저장
    save_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return batch_image
#----------------------------------------------#
# settind : 최적의 model 불러오고, class_name과 class_explain 선언
def setting():
    # 모델 로드 및 예측

    class_name=[["Ac","고적운"],["As","고층운 "],["Cb","적란운 "],["Cc","권적운"],["Ci","권운"],["Cs","권층운"],["Ct","비행운"],["Cu","적운"],["Ns","난층운 "],["Sc","층적운"]]
    class_explain=[
        "고적운은 높쌘구름, 양떼구름이라고도 하며, 강수를 포함하고 있지 않아 맑은 날씨를 예상할수있어구리.",
        "고층운은 높층구름, 흰색차일구름 이라고도 하며, 주로 흐린날씨에 나타나는 구름이야구리. 약한 비나 눈이 내릴수 있겠어구리.",
        "적란운은 쌘비구름 이라고도 하며, 주로 소나기를 동반하고, 심할 경우 우박과 뇌우, 더 심할 경우 용오름을 동반해구리. 구름속에 전하가 모여있어 번개도 동반해서 뇌운이라고도 불러구리. 비, 우박, 토네이도에 주의해구리!",
        "권적운은 털쌘구름, 비늘구름, 조개구름이라고도 하며, 구름 자체가 강수를 가지고 있지는 않지만 강수가 있을 것이라는 징조로 볼 수 있어구리. 날씨가 맑지만 추울 것으로 예상돼구리.",
        "권운은 대부분 얼음결정으로 이루어진 섬세하고 깃털 같은 구름이야구리. 가느다란 모양은 강한 바람으로 생긴거야구리. 날씨 변화가 다가오고 있어구리!",
        "권층운은 겨울에 가장 흔하게 볼 수 있는 구름이야구리. 24시간 이내에 비나 눈이 내릴 수도 있겠어구리.",
        "비행운은 고공 비행하는 제트기가 지나가고 남은 구름이야구리. 제트 엔진의 배기가스에서 나오는 수증기가 응축된 물방울로 만들어 졌기 때문에 여전히 구름이야구리.",
        "적운은 쌘구름, 뭉게구름 이라고도 하며, 날씨가 맑고 한낮 기온이 높을 경우 고기압권에서 대류작용으로 형성되는 구름이야구리.",
        "난층운은 비층구름, 비구름이라고도 하며, 비교적 낮은 고도에서 하늘을 가득 채운 짙은 회색빛의 먹구름이야구리. 비나 눈이 계속 내릴 것 같아구리.",
        "층적운은 두루마리구름이라고도 하며, 종종 어두운 벌집처럼 보이는 회색 또는 흰색의 얼룩덜룩한 구름이야구리. 날씨가 지금은 좋지만 폭풍이 올 수도 있을 것 같아구리."
    ]
    return class_name,class_explain
#----------------------------------------------#
# test_accuracy : 웹에 업로드된 사진 분류 진행!
def test_accuracy(uploaded_file):

    batch_image=upload_image(uploaded_file)
    class_name, class_explain = setting()
    pred_proba = model.predict(batch_image) # 전체 클래스에 대해서


    pred = np.argmax(pred_proba)
    print(pred)
    print(pred_proba)
    pred_proba = pred_proba[0]
    print(pred_proba)
    pred_max_proba=pred_proba[pred] # 최대 확률 값 return
    pred_label=class_name[pred][0]
    pred_class_name = class_name[pred][1] # 최대 확률 값을 가진 class의 이름(ex.난층운) return
    pred_explanation= class_explain[pred] # 해당 class의 설명 return (ex.해당 구름은 ~~뒤에 비가 옵니다)
    # images_name=class_sample_image(pred_label) # 화면에 표시될 sample image의 주소

    return pred_max_proba, pred_class_name, pred_explanation
#----------------------------------------------#
# # class_sample_image : 해당 구름 sample 이미지!
# def class_sample_image(pred_label):
#     filepath = f'./show_image/{pred_label}'
#     image_names = []
#     try:
#         for file_name in os.listdir(filepath):
#             if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
#                 image_names.append(file_name)
#     except FileNotFoundError:
#         print(f"Error: Directory '{filepath}' does not exist.")
#     return image_names

