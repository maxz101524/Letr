import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import fitz # PyMuPDF
from io import BytesIO

# --- Load API key ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Streamlit Config ---
st.set_page_config(page_title="NetReach.AI", page_icon=":robot_face:", layout="wide")
st.title("NetReach.AI - Cold Email Generator")

# Initialize session state
if 'user_background' not in st.session_state:
    st.session_state.user_background = ""
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set()

# --- INPUTS ---
upload_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    try:
        # Read the PDF file bytes
        pdf_bytes = file.read()
        # Create a BytesIO object
        pdf_stream = BytesIO(pdf_bytes)
        # Open PDF from memory buffer
        with fitz.open(stream=pdf_stream, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

def generate_resume_summary(resume_text):
    """Generate a summary from resume text using GPT."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume analyzer. Create a concise summary of the person's background, skills, and experience based on their resume."},
                {"role": "user", "content": f"Please analyze this resume and create a concise summary (3-4 sentences) highlighting the person's background, skills, and experience:\n\n{resume_text}"}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return ""

st.header("Tell me about yourself")
user_background = st.text_area("Your background or resume summary", value=st.session_state.user_background)

if upload_resume is not None:
    # Create a unique identifier for the file
    file_id = upload_resume.name + str(upload_resume.size)

    if st.session_state.get("last_file_id") != file_id:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(upload_resume)
            if resume_text:
                summary = generate_resume_summary(resume_text)
                if summary:
                    st.session_state.user_background = summary
                    st.session_state.last_file_id = file_id
                    st.rerun()

st.header("Who are you contacting?")
recipient = st.text_input("Recipient's name + role")
goal = st.selectbox("Goal of your message", ["Ask for a referral", "Request a coffee chat", "Seek resume feedback", "Other"])
tone = st.selectbox("Preferred tone", ["Friendly", "Curious", "Professional"])

# Add a clear button to reset the form
if st.button("Clear Form"):
    st.session_state.user_background = ""
    st.session_state.last_file_id = None
    st.rerun()

# --- GENERATE ---
if st.button("Generate Cold Email") and user_background and recipient:
    with st.spinner("Writing your message..."):
        prompt = f"""
        Write a personalized cold outreach email (120-150 words) with a {tone.lower()} tone.
        The sender's background: {user_background}
        The recipient: {recipient}
        Goal: {goal}
        Make it sound human and not robotic. No need for subject line.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            result = response.choices[0].message.content
            st.success("Here's your message:")
            st.text_area("Cold Email", result, height=200)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
else:
    st.info("Please fill in both your background and recipient info to generate.")
