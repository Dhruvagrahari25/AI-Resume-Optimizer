from dotenv import load_dotenv
load_dotenv()
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input, pdf_content, prompt):
#     model=genai.GenerativeModel('gemini-pro-vision')
#     response = model.generate_content(input,pdf_content[0],prompt)
#     return response.text
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:    
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        #convert to bytes
        img_bytes_arr = io.BytesIO()
        first_page.save(img_bytes_arr, format='JPEG')
        img_bytes_arr = img_bytes_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes_arr).decode() # encode to base 64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

##Streamlit APP
st.set_page_config(page_title="Resume ATS",page_icon=':books:')
st.header("Resume ATS System")
input_text = st.text_area("Enter Job Description",  key="input")
uploaded_file = st.file_uploader("Upload Your resume (PDF) ", type=["pdf"])

if uploaded_file is not None: 
    st.write("PDF uploaded Successfully!")

submit1 = st.button("Tell me about the Resume")

# submit2 = st.button("How can i improve my skills")

# submit3 = st.button("What are the missing keywords?")

submit2 = st.button("Percentage match")

input_prompt1 = """
    As an experienced HR professional specializing in Data Science, Full Stack Web Development, Big Data Engineering, DevOps, and Data Analysis, your task is to review the provided resume in relation to the specified job requirements. Here's how you can proceed:
    Objective:
    Assess the candidate's qualifications, skills, and experience.
    Determine alignment with the job description.
    Process:
    Step 1: Carefully read the job description.
    Step 2: Analyze the candidate's resume.
    Step 3: Evaluate strengths and weaknesses based on the following criteria:
    Strengths: Highlight relevant skills, experience, and achievements.
    Weaknesses: Identify any gaps or missing qualifications.
    Professional Evaluation:
    Provide a concise assessment of how well the candidate's profile aligns with the job requirements.
    Mention specific strengths and areas for improvement.
    Remember to consider both hard skills (technical expertise) and soft skills (communication, teamwork, adaptability) during your evaluation
"""


input_prompt2 = """
    "You are a skilled at ATS (Application Tracking System) scanner with a deep understanding of Data science, full stack web development, big data engineering, devops, data analysis and deep ats functionality. 
    Your task is to evaluate the resume against the provided job description. Give me the percentage match of the job description. First, the output should come as percentage and keyword missing."
    Objective: Compare the candidate's resume with the provided job description to determine the suitability and alignment.
    Process:
    Step 1: Extract keywords and skills from the job description.
    Step 2: Analyze the resume for relevant keywords and skills.
    Step 3: Calculate the percentage match based on the presence of these keywords.
    Step 4: Identify any missing critical keywords or skills.
    Output:
    Match Percentage: A numerical score (e.g., 80%) indicating how closely the resume aligns with the job requirements.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is :")
        st.write(response)
    else:
        st.write("Please upload a Resume !")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is :")
        st.write(response)
    else:
        st.write("Please upload a Resume !")
    