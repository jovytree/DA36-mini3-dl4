import streamlit as st
import module # 기능 구현을 위해 만들어놓은 module.py를 import 합니다
import time


# 세션 상태를 사용하여 페이지를 추적
if 'page' not in st.session_state:
    st.session_state.page = 'home'  # 기본 페이지는 'home'

# 홈 페이지
if st.session_state.page == 'home':
    st.image("./png/모동숲.jpg", use_container_width=True)
    # 구름 분류 버튼
    if st.button('구름 분류 GO! GO!', icon = "👉", use_container_width=True):
        st.session_state.page = 'cloud'  # 버튼 클릭 시 페이지 변경

# 구름 분류 페이지
elif st.session_state.page == 'cloud':
    # '홈으로 돌아가기' 버튼
    if st.button('홈으로 돌아가기', icon='🏠', use_container_width=True):
        st.session_state.page = 'home'  # 버튼 클릭 시 홈 페이지로 이동

    st.image("./png/너굴.png", use_container_width=False)
    texts = [
        "🦝너굴🦝 : **어서와, 구리!**",
        "🦝너굴🦝  : **구름을 분류하고 싶어구리?**",
        "🦝너굴🦝  : **그럼...**",
        "🦝너굴🦝  : **여기에 구름 사진을 업로드 해봐구리!**"
    ]

    # 텍스트를 한 줄씩 출력
    for text in texts:
        st.write(text)  # 텍스트 출력
        time.sleep(2)  # 2초 지연

    # 사진 업로드
    uploaded_file = st.file_uploader("⛅구름 사진을 업로드하세요.⛅", type=["jpg", "png", "jpeg"])
    print(type(uploaded_file))

    if uploaded_file is not None:
        # pred = 예측
        pred_max_proba,pred_class_name,pred_explanation,images_name=module.test_accuracy(uploaded_file)

        st.write("파일 이름:", uploaded_file.name)
        st.write("파일 타입:", uploaded_file.type)
        st.write("파일 크기:", uploaded_file.size, "bytes")

        st.image(uploaded_file, caption="업로드 이미지")

        texts = [
            f"🦝너굴🦝  : 위 사진은 **{pred_class_name}** 일 확률이 **{pred_max_proba:.4f}** 이야 구리.",
            f"🦝너굴🦝  : {pred_explanation}"
        ]

        # 텍스트를 한 줄씩 출력
        for text in texts:
            st.write(text)  # 텍스트 출력
            time.sleep(2)  # 2초 지연

