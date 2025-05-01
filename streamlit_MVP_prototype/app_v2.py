import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import fitz # PyMuPDF
from io import BytesIO
from datetime import datetime, timedelta
import pytz

# --- Load API key ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Streamlit Config ---
st.set_page_config(page_title="NetReach.AI v2", page_icon=":robot_face:", layout="wide")

# Initialize session state
if 'user_background' not in st.session_state:
    st.session_state.user_background = ""
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set()

def get_smart_suggestions(goal, recipient_context):
    """Generate smart suggestions based on the email context."""
    suggestions = {
        "Ask for a referral": {
            "best_times": ["Tuesday-Thursday", "10 AM - 2 PM local time"],
            "optimal_length": "100-130 words (shorter is better for referral requests)",
            "tips": [
                "Mention how you found their profile/work",
                "Be specific about which role/team you're interested in",
                "Make it easy for them to refer you with a clear ask"
            ]
        },
        "Request a coffee chat": {
            "best_times": ["Tuesday-Thursday", "2 PM - 4 PM local time"],
            "optimal_length": "120-150 words",
            "tips": [
                "Suggest specific dates/times",
                "Offer both virtual and in-person options",
                "Mention specific topics you'd like to discuss"
            ]
        },
        "Seek resume feedback": {
            "best_times": ["Tuesday-Wednesday", "11 AM - 3 PM local time"],
            "optimal_length": "130-160 words",
            "tips": [
                "Highlight specific areas you'd like feedback on",
                "Mention why their expertise matters",
                "Offer to keep it brief (15 minutes)"
            ]
        }
    }
    
    # Get base suggestions for the goal
    base_suggestions = suggestions.get(goal, {
        "best_times": ["Tuesday-Thursday", "10 AM - 2 PM local time"],
        "optimal_length": "120-150 words",
        "tips": [
            "Be specific about your request",
            "Show you've done your research",
            "Make the value proposition clear"
        ]
    })
    
    # Add context-based tips
    if recipient_context:
        if "talk" in recipient_context.lower() or "speaker" in recipient_context.lower():
            base_suggestions["tips"].append("Reference specific points from their talk/presentation")
        if "article" in recipient_context.lower() or "post" in recipient_context.lower():
            base_suggestions["tips"].append("Mention specific insights from their writing")
        if "worked" in recipient_context.lower() or "company" in recipient_context.lower():
            base_suggestions["tips"].append("Leverage your shared professional background")
            
    return base_suggestions

# Main app layout
col1, col2 = st.columns([2, 1])

with col1:
    st.title("NetReach.AI - Cold Email Generator v2")
    st.caption("Enhanced with Smart Suggestions")
    
    # --- INPUTS ---
    upload_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    def extract_text_from_pdf(file):
        """Extract text from a PDF file."""
        try:
            pdf_bytes = file.read()
            pdf_stream = BytesIO(pdf_bytes)
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
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional resume analyzer. Create a concise summary of the person's background, skills, and experience based on their resume. This information will be used to generate a cold email or other similar message."},
                    {"role": "user", "content": f"Please analyze this resume and create a concise summary highlighting the person's background, skills, and experience:\n\n{resume_text}"}
                ],
                temperature=0.5,
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error generating summary: {e}")
            return ""

    st.header("Tell me about yourself")
    user_background = st.text_area("Your background or resume summary", value=st.session_state.user_background)
    st.markdown("Feel free to edit the auto-generated summary to better suit your needs.")

    if upload_resume is not None:
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
    recipient = st.text_input("Recipient's name")
    recipient_context = st.text_area(
        "Additional context about the recipient (optional)",
        help="E.g., their background, recent achievements, mutual connections, why you chose them, or anything you found interesting about their work",
        placeholder="Example: They recently gave a talk about AI ethics at Stanford. We both worked at Google but at different times. I really enjoyed their recent article about machine learning in healthcare."
    )

    # Goal selection with custom option
    goal_options = ["Ask for a referral", "Request a coffee chat", "Seek resume feedback", "Other (custom)"]
    goal_selection = st.selectbox("Goal of your message", goal_options)

    if goal_selection == "Other (custom)":
        custom_goal = st.text_input("Enter your custom goal", placeholder="E.g., Discuss potential collaboration opportunity")
        goal = custom_goal
    else:
        goal = goal_selection

    # Tone selection with custom option
    tone_options = ["Friendly", "Curious", "Professional", "Other (custom)"]
    tone_selection = st.selectbox("Preferred tone", tone_options)

    if tone_selection == "Other (custom)":
        custom_tone = st.text_input("Enter your preferred tone", placeholder="E.g., Enthusiastic, Humble, Direct")
        tone = custom_tone
    else:
        tone = tone_selection

    # Add a clear button to reset the form
    if st.button("Clear Form"):
        st.session_state.user_background = ""
        st.session_state.last_file_id = None
        st.rerun()

    # --- GENERATE ---
    if st.button("Generate Cold Email") and user_background and recipient:
        with st.spinner("Writing your message..."):
            context_prompt = f"\nAdditional context about the recipient: {recipient_context}" if recipient_context else ""
            prompt = f"""
            You are an expert in professional communication and relationship building. Create a highly personalized cold outreach email that will genuinely connect with the recipient and stand out from generic messages.

            Key requirements:
            - Length: 120-150 words
            - Tone: {tone.lower()}
            - Primary goal: {goal}

            Sender's background: {user_background}
            Recipient: {recipient}{context_prompt}

            Guidelines for crafting the message:
            1. Start with a specific, personalized opening that shows you've done your homework
            2. Establish a clear, authentic connection between your background and their work/expertise
            3. Be specific about why you chose them (not just anyone in their position)
            4. Make your {goal.lower()} request clear but not demanding
            5. Provide clear value proposition or mutual benefit where appropriate
            6. Keep the focus on quality of connection over asking for favors
            7. Avoid generic phrases like "I hope this email finds you well" or "I would love to pick your brain"
            8. Be concise and respectful of their time

            Write the email body only (no subject line needed). Make it sound natural and conversational, not formulaic.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert email writer who crafts highly personalized, authentic cold outreach messages that build genuine connections."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )
                result = response.choices[0].message.content
                st.success(f"Here's your message, go get that {goal}!:")
                st.text_area("Cold Email", result, height=200)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.info("Please fill in both your background and recipient info to generate.")

# Smart Suggestions Sidebar
with col2:
    if recipient_context or goal_selection:
        st.header("? Smart Suggestions")
        suggestions = get_smart_suggestions(goal_selection, recipient_context)
        
        with st.expander("? Best Practices", expanded=True):
            st.subheader("Best Time to Send")
            st.write("? Days: " + suggestions["best_times"][0])
            st.write("? Hours: " + suggestions["best_times"][1])
            
            st.subheader("Optimal Length")
            st.write("? " + suggestions["optimal_length"])
        
        with st.expander("? Pro Tips", expanded=True):
            for tip in suggestions["tips"]:
                st.write("? " + tip)

        # Calculate best send time
        with st.expander("? Send Time Calculator", expanded=True):
            now = datetime.now(pytz.UTC)
            recipient_tz = st.selectbox(
                "Recipient's Timezone",
                options=["US/Pacific", "US/Mountain", "US/Central", "US/Eastern"],
                help="Select the recipient's timezone to get the best send time"
            )
            
            if recipient_tz:
                local_tz = pytz.timezone(recipient_tz)
                local_time = now.astimezone(local_tz)
                
                # Find next optimal send time
                days_map = {
                    "Tuesday-Thursday": [1, 2, 3],
                    "Tuesday-Wednesday": [1, 2]
                }
                target_days = days_map.get(suggestions["best_times"][0], [1, 2, 3])
                
                # Calculate next optimal day
                days_until_target = 0
                current_weekday = local_time.weekday()
                while current_weekday + days_until_target not in target_days:
                    days_until_target += 1
                    if current_weekday + days_until_target > 6:
                        current_weekday = -days_until_target
                
                optimal_time = local_time.replace(hour=11, minute=0) + timedelta(days=days_until_target)
                
                st.write("? Next optimal send time:")
                st.info(f"{optimal_time.strftime('%A, %B %d at %I:%M %p')} {local_tz.zone}")
