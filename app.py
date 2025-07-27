import streamlit as st
from quiz_generator import generate_vocab_quiz
from t2s import speak_thai
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="AI Thai Learning Companion", layout="centered")
st.title("🧠 AI Thai Learning Companion")
st.subheader("ฝึกภาษาไทยด้วย AI")

if "quizzes" not in st.session_state:
    st.session_state.quizzes = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

user_text = st.text_area("✍️ ใส่ข้อความภาษาไทยของคุณ:", height=200)

if st.button("🔍 สร้างคำถามคำศัพท์"):
    if not user_text.strip():
        st.warning("กรุณาใส่ข้อความก่อน")
    else:
        st.session_state.quizzes = generate_vocab_quiz(user_text)
        st.session_state.answers = {}
        st.success("สร้างคำถามแล้ว")

# Show quizzes if any
for idx, q in enumerate(st.session_state.quizzes):
    with st.expander(f"❓ คำถาม {idx+1}"):
        st.write(q["question"])

        if st.button(f"🔈 ฟังคำถาม {idx+1}", key=f"tts-{idx}"):
            audio_file = speak_thai(q["question"])
            with open(audio_file, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                audio_html = f"""
                <audio autoplay controls>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
                components.html(audio_html, height=60)

        selected = st.radio("เลือกคำตอบของคุณ:", q["choices"], 
                           key=f"radio-{idx}",
                           index=(q["choices"].index(st.session_state.answers.get(idx)) 
                                  if st.session_state.answers.get(idx) in q["choices"] else 0))
        st.session_state.answers[idx] = selected

        if st.button("✅ ตรวจคำตอบ", key=f"check-{idx}"):
            if st.session_state.answers.get(idx) == q["answer"]:
                st.success("✅ ถูกต้อง")
            else:
                st.error(f"❌ คำตอบที่ถูกต้อง คือ {q['answer']}")