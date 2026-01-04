import streamlit as st
import PyPDF2
import pandas as pd
import re

st.set_page_config(page_title="Turner Universal ATS - Application Tracking System", page_icon="📄")

st.title("📄 Turner Universal ATS Resume Checker")

resume_files = st.file_uploader(
    "📤 Upload Multiple Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

job_desc = st.text_area("🧾 Paste Job Description")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

def tokenize(text):
    return set(re.findall(r"\b[a-zA-Z]{2,}\b", text))

def calculate_ats_score(resume_text, job_desc):
    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_desc.lower())

    matched = resume_tokens.intersection(job_tokens)
    missing = job_tokens - resume_tokens

    score = (len(matched) / len(job_tokens)) * 100 if job_tokens else 0
    return round(score, 2), matched, missing

if st.button("🔍 Analyze Resumes"):
    if resume_files and job_desc:
        results = []

        for resume in resume_files:
            resume_text = extract_text_from_pdf(resume)
            score, matched, missing = calculate_ats_score(resume_text, job_desc)

            results.append({
                "Resume Name": resume.name,
                "ATS Match 100 out ⬇️": score,
                "Matched Keywords": len(matched),
                "Missing Keywords": len(missing)
            })

        df = pd.DataFrame(results).sort_values(
            by="ATS Match 100 out ⬇️",
            ascending=False
        )

        st.subheader("📊 Resume ATS Ranking")
        st.dataframe(df, use_container_width=True)

        st.subheader("❌ Missing Keywords (Top 20)")
        for resume in resume_files:
            resume_text = extract_text_from_pdf(resume)
            _, _, missing = calculate_ats_score(resume_text, job_desc)

            st.write(f"**{resume.name}**")
            st.write(", ".join(list(missing)[:20]))

    else:
        st.warning("Upload resumes and paste job description")

st.markdown("---")
st.caption("Built by Tanmay Gaikwad | Turner Universal ATS")