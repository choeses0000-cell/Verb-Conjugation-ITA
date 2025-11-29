import streamlit as st
from mlconjug3 import Conjugator
import pdfplumber
import docx

# 이탈리아어 동사 분석 함수
def extract_verbs(text):
    words = text.split()
    conjugator = Conjugator(language='it')
    verbs = []

    for w in words:
        try:
            info = conjugator.conjugate(w)
            if info:
                verbs.append({
                    "verb": w,
                    "presente": info.conjug_info['indicativo']['presente'],
                    "passato_prossimo": info.conjug_info['indicativo']['passato prossimo']
                })
        except:
            pass
    return verbs

# 파일 텍스트 추출
def read_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages)
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    else:
        return None

# Streamlit UI
st.title("🇮🇹 Italian Verb Conjugation Extractor")

st.write("텍스트를 직접 붙여넣거나 파일을 업로드하세요.")

# 🔹 텍스트 입력
text_input = st.text_area("텍스트 직접 입력", height=200)

# 🔹 파일 업로드
uploaded_file = st.file_uploader("또는 파일을 업로드하세요 (.txt, .docx, .pdf)", type=["txt", "docx", "pdf"])

# 🔹 버튼
if st.button("동사 분석하기"):
    text = ""

    if text_input.strip():
        text = text_input
    elif uploaded_file is not None:
        text = read_file(uploaded_file)
    else:
        st.error("텍스트나 파일 중 하나를 입력하세요!")
        st.stop()

    verbs = extract_verbs(text)

    if not verbs:
        st.warning("동사를 찾지 못했습니다.")
    else:
        st.success(f"{len(verbs)}개의 동사가 발견되었습니다.")
        for v in verbs:
            st.write(f"### 🔹 동사: {v['verb']}")
            st.json({
                "Presente": v["presente"],
                "Passato Prossimo": v["passato_prossimo"]
            })
