import streamlit as st
import matplotlib.pyplot as plt
from utils import *

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer")
st.write("Analyze your resume with AI and get insights")

# Sidebar
st.sidebar.header("Upload Files")
resume_file = st.sidebar.file_uploader("Upload Resume", type=["pdf","docx"])
job_desc = st.sidebar.text_area(
    "Paste Job Description",
    height=300  # 👈 this adds scrollbar automatically
)

if resume_file and job_desc:

    # Extract text
    if resume_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_file)
    else:
        resume_text = extract_text_from_docx(resume_file)

    # Clean text
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_desc)

    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_desc)

    # Similarity
    score = calculate_similarity(resume_clean, jd_clean)

    # Missing skills
    missing = missing_skills(resume_skills, jd_skills)

    # UI Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Resume Score")
        st.progress(int(score))
        st.write(f"**Match Score:** {score:.2f}%")

        st.subheader("✅ Your Skills")
        st.write(resume_skills)

        st.subheader("❌ Missing Skills")
        st.write(missing)

    with col2:
        st.subheader("📈 Skill Comparison")

        labels = ["Matched Skills", "Missing Skills"]
        values = [len(resume_skills), len(missing)]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig)

    # Suggestions
    st.subheader("💡 Suggestions")
    if score > 80:
        st.success("Excellent match! You're ready to apply 🚀")
    elif score > 50:
        st.warning("Good, but you can improve your resume.")
    else:
        st.error("Low match. Add missing skills and improve content.")

else:
    st.info("Upload resume and paste job description to start analysis.")