import streamlit as st
import pymongo
import os
import PyPDF2
import pandas as pd
# from google import genai
import google.generativeai as genai


def keywords_list_api(text):
    client = genai.Client(api_key="AIzaSyCqq5SZhuK3YtvnH1joGUSmdTtqep7qK10")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"Extract the keywords and provide a json object with just a single key value {text}"
    )
    list = response.text
    start = list.find("[")
    last = list.rfind("]")
    list = list[start+1:last]
    list = list.split(",")
    return list

def generate_cv_review(cv_text):
    """Uses an LLM to review a CV and generate structured feedback."""
    client = genai.Client(api_key="AIzaSyCqq5SZhuK3YtvnH1joGUSmdTtqep7qK10")

    prompt = f"""
    You are an AI-powered CV reviewer. Given the following CV text, analyze it and return:
    - A score out of 10 based on completeness, clarity, and relevance.
    - Key strengths of the candidate.
    - Missing skills or areas of improvement.
    - Any suggestions to enhance the CV.

    Respond in JSON format with the following keys:
    {{
        "score": (integer),
        "strengths": (list of key strengths),
        "missing_skills": (list of missing skills),
        "suggestions": (list of improvement suggestions)
    }}

    CV Text:
    {cv_text}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    try:
        review = eval(response.text)  # Convert string to dictionary
    except:
        review = {
            "score": 0,
            "strengths": [],
            "missing_skills": [],
            "suggestions": ["Could not generate a review. Please try again."]
        }

    return review

def rescore(searchwords, cv):
    extra_score = 0
    weight = 2  # Weight for each keyword match
    for i in searchwords:
        for j in cv['keywords']:
            if i.lower() in j.lower() or j.lower() in i.lower():
                extra_score += weight
    cv["extra_score"] = extra_score
    return cv

def update_extra_scores(keywords):
    cv_documents = list(cv_col.find({}))
    
    for cv in cv_documents:
        updated_cv = rescore(keywords, cv)
        
        cv_col.update_one(
            {"_id": cv["_id"]},
            {"$set": {"extra_score": updated_cv["extra_score"]}}
        )

def display_cvs(cv_documents):
    if cv_documents:
        for cv in cv_documents:
            st.subheader(f"CV: {cv['file_name']}")
            st.write(f"*Review Score:* {cv.get('review_score', 'N/A')}/10")
            st.write(f"*Strengths:* {', '.join(cv.get('strengths', []))}")
            st.write(f"*Missing Skills:* {', '.join(cv.get('missing_skills', []))}")
            st.write(f"*Suggestions:*")
            for suggestion in cv.get("suggestions", []):
                st.write(f"- {suggestion}")

            st.write("---")

    else:
        st.info("No CVs found.")

def display_jds(jd_documents):
    if jd_documents:
        jd_df = pd.DataFrame(jd_documents)
        st.dataframe(jd_df)
    else:
        st.info("No job descriptions found.")

# --- MongoDB Configuration ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "capstone"

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    jd_col = db['jd_col']
    cv_col = db['cv_col']
    st.success("Connected to MongoDB")
except Exception as e:
    st.error(f"Could not connect to MongoDB: {e}")
    st.stop()

# --- Streamlit App ---
st.title("CV Reviewer")

jd = st.text_area("Enter your job description:", height=150)
uploaded_files = st.file_uploader("Upload CVs (PDF files)", type="pdf", accept_multiple_files=True)

if st.button("Save Data"):
    if jd:
        keywords_jd = keywords_list_api(jd)
        jd_data = {"job_description": jd, "keywords": keywords_jd}
        jd_col.insert_one(jd_data)
        st.success("Job description saved to MongoDB!")
    else:
        st.warning("Please enter a job description.")

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                pdf_text = "".join([page.extract_text() for page in pdf_reader.pages])

                base_score = 0
                keywords_cv = keywords_list_api(pdf_text)

                for i in jd_data['keywords']:
                    for j in keywords_cv:
                        if i.lower() in j.lower() or j.lower() in i.lower():
                            base_score += 1

                # Generate CV review using LLM
                review = generate_cv_review(pdf_text)

                cv_data = {
                    "file_name": uploaded_file.name,
                    "text": pdf_text,
                    "keywords": keywords_cv,
                    "base_score": base_score,
                    "extra_score": 0,
                    "review_score": review["score"],
                    "strengths": review["strengths"],
                    "missing_skills": review["missing_skills"],
                    "suggestions": review["suggestions"],
                }

                cv_col.insert_one(cv_data)
                st.success(f"CV '{uploaded_file.name}' saved and reviewed!")

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
    else:
        st.warning("No PDF files uploaded.")

if st.button("clear"):
    jd_col.delete_many({})
    cv_col.delete_many({})
    st.info("Cleared existing data in 'jd_col' and 'cv_col' collections.")

jd_documents = list(jd_col.find({}, {"_id": 0, "keywords": 0}))
display_jds(jd_documents)

st.title("Keyword Input")

if "keywords" not in st.session_state:
    st.session_state.keywords = []

keyword = st.text_input("Enter a keyword:")

if keyword:
    if keyword not in st.session_state.keywords:
        st.session_state.keywords.append(keyword)
        st.success(f"Keyword '{keyword}' added!")
        update_extra_scores(st.session_state.keywords)
    else:
        st.warning(f"Keyword '{keyword}' is already in the list.")

if st.session_state.keywords:
    st.write("*Keywords List:*")
    for i, kw in enumerate(st.session_state.keywords):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(kw)
        with col2:
            if st.button("Delete", key=f"delete_{i}"):
                del st.session_state.keywords[i]
                update_extra_scores(st.session_state.keywords)

cv_documents = list(cv_col.find({}, {"_id": 0}))
display_cvs(cv_documents)

if client:
    client.close()