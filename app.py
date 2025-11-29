import streamlit as st
from mlconjug3 import Conjugator
import re

# --- Word, PDF 파일 읽기 위한 라이브러리 ---
import docx2txt          # .docx 파일 읽기
from io import StringIO
import PyPDF2            # PDF 텍스트 추출

st.title("Italian Verb Analyzer")
st.write("📄 업로드한 파일(Word/PDF/TXT)에서 이탈리아어 동사를 추출해 Presente / Passato Prossimo 변화를 보여줍니다.")

# 업로드 허용 파일 확장자
uploaded_file = st.file_uploader("파일(.txt, .docx, .pdf)을 업로드하세요", type=["txt", "docx", "pdf"])

def extract_text_from_file(file):
    """파일 확장자별 텍스트 추출 함수"""
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    elif file.name.endswith(".docx"):
        return docx2txt.process(file)

    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    return ""

if uploaded_file:
    text = extract_text_from_file(uploaded_file)

    st.subheader("📄 추출된 텍스트")
    st.write(text)

    # --- 동사 후보 추출 ---
    st.subheader("🔍 추출된 동사 후보 (부정형)")

    tokens = re.findall(r"\b[a-zA-Zàèéìòù]+?\b", text.lower())
    infinitive_candidates = [t for t in tokens if t.endswith(("are", "ere", "ire"))]
    infinitive_candidates = list(set(infinitive_candidates))

    if infinitive_candidates:
        st.write(infinitive_candidates)
    else:
        st.write("부정형 동사를 찾을 수 없습니다.")

    # --- 동사 변화 ---
    st.subheader("📌 동사 변화 결과")

    conj = Conjugator(language="it")

    for verb in infinitive_candidates:
        st.markdown(f"### 🔹 **{verb}**")
        try:
            result = conj.conjugate(verb)

            # Presente
            st.write("**Presente (현재형):**")
            presente = result.conjug_info['Indicativo']['Presente']
            for person, form in presente.items():
                st.write(f"- {person}: {form}")

            # Passato Prossimo
            st.write("**Passato Prossimo (근과거):**")
            passato = result.conjug_info['Indicativo']['Passato Prossimo']
            for person, form in passato.items():
                st.write(f"- {person}: {form}")

        except:
            st.error(f"{verb} 변환 실패 — 사전에 없거나 규칙 밖 동사일 수 있습니다.")
