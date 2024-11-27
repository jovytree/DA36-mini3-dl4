import streamlit as st
import module # 기능 구현을 위해 만들어놓은 module.py를 import 합니다

st.write("하늘 이미지를 업로드하면, 날씨를 예측해 드립니다.")
uploaded_file = st.file_uploader("하늘 이미지 파일을 업로드하세요.", type=["jpg", "png", "jpeg"])
print(type(uploaded_file))

if uploaded_file is not None:
    # pred = 예측
    pred_max_proba,pred_class_name,pred_explanation,images_name=module.test_accuracy(uploaded_file)
    
    st.write("파일 이름:", uploaded_file.name)
    st.write("파일 타입:", uploaded_file.type)
    st.write("파일 크기:", uploaded_file.size, "bytes")

    st.image(uploaded_file, caption="업로드 이미지")

    
    st.success(f"위 사진은 {pred_class_name} 일 확률이 {pred_max_proba:.4f} 입니다. 특징은 ........입니다.")

