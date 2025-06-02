import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import fitz # PyMuPDF
from io import BytesIO

# --- Load API key ---
load_dotenv()

# Try to get API key from multiple sources
api_key = None

# First, try Streamlit secrets (for Streamlit Cloud deployment)
try:
    if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
except:
    pass

# If not found in secrets, try environment variables (for local development)
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API key not found! Please set your OPENAI_API_KEY in Streamlit secrets (for cloud deployment) or in your .env file (for local development).")
    st.stop()

client = OpenAI(api_key=api_key)

# --- Streamlit Config ---
st.set_page_config(page_title="NetReach.AI", page_icon="📧", layout="wide")

# Custom fonts and CSS styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Custom font */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove extra padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom app header */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-radius: 0 0 20px 20px;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Section containers */
    .section-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0 0 2rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Section headers with better spacing */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.8rem;
    }
    
    /* Better spacing for content within sections */
    .section-container .stMarkdown {
        margin-bottom: 1rem;
    }
    
    /* Improved input spacing */
    .stTextInput, .stTextArea, .stSelectbox {
        margin-bottom: 1rem;
    }
    
    /* Remove any unwanted margins on first elements */
    .section-container:first-child {
        margin-top: 0;
    }
    
    /* Ensure no extra spacing from columns */
    .element-container:empty {
        display: none;
    }
    
    /* Better expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Step dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    /* Custom buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 10px !important;
        border: 2px solid #e1e5e9 !important;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Progress bars and spinners */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        border-radius: 10px;
    }
    
    /* Warning message styling */
    .stWarning {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_background' not in st.session_state:
    st.session_state.user_background = ""
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set()

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
                {"role": "system", "content": """You are an expert career strategist and networking coach who specializes in helping people craft compelling personal narratives for professional outreach. Your goal is to transform resume information into authentic, conversational summaries that highlight what makes someone genuinely interesting and valuable to connect with.

Key principles:
1. Write in first person, conversational tone (as if the person is introducing themselves)
2. Focus on unique experiences, impact, and passion rather than just listing credentials
3. Highlight specific achievements with quantifiable impact when possible
4. Identify transferable skills and emerging market trends they're aligned with
5. Include personality indicators and genuine interests
6. Make it suitable for networking conversations, not job applications
7. Since this information will be fed to an AI to generate a cold email, make it as detailed and specific as needed, word count is not a concern. The more detail you provide, the better and less generic the message will be"""},
                {"role": "user", "content": f"""Transform this resume into a compelling personal introduction that someone would use when networking or reaching out to industry professionals. Focus on:

- What makes them uniquely interesting or valuable
- Specific achievements with measurable impact
- Current market-relevant skills and trends they're working with
- Their genuine interests and what drives them
- How their diverse experiences create a unique perspective

Write in first person as if they're introducing themselves. Make it conversational, authentic, and networking-focused rather than formal or job-application-style.

Resume content:
{resume_text}

Example style: "I'm a data science student at UIUC who's been fascinated by how AI can solve real-world problems. I recently built predictive models that improved public health planning efficiency by 30% during my research at the Health Informatics Center, and I'm currently exploring how machine learning can optimize energy grids after my internship in Shanghai. What really drives me is finding creative ways to apply algorithms to make systems more efficient and impactful."

Now create a similar authentic introduction based on this person's actual background:"""}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return ""

# Custom header
st.markdown("""
<div class="main-header">
    <h1>📧 NetReach.AI</h1>
    <p>Generate personalized cold emails that actually get responses</p>
</div>
""", unsafe_allow_html=True)

# Step-by-step flow with full-width sections
st.markdown("---")

# STEP 1: Your Information
st.markdown('<div class="section-container"><div class="section-header">📝 Step 1: Your Information</div>', unsafe_allow_html=True)

st.markdown("**📄 Upload Resume (Optional)**")
upload_resume = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
st.caption("💡 Upload your resume for an AI-generated summary, or write your own below")

if upload_resume is not None:
    file_id = upload_resume.name + str(upload_resume.size)
    if st.session_state.get("last_file_id") != file_id:
        with st.spinner("🤖 Analyzing your resume..."):
            resume_text = extract_text_from_pdf(upload_resume)
            if resume_text:
                summary = generate_resume_summary(resume_text)
                if summary:
                    st.session_state.user_background = summary
                    st.session_state.last_file_id = file_id
                    st.rerun()

st.markdown("**✍️ Tell us about yourself**")
user_background = st.text_area(
    "", 
    value=st.session_state.user_background,
    placeholder="Describe your background, experience, and what makes you unique. The more detail you provide, the better and less generic the message will be",
    height=120,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# STEP 2: Recipient Information
st.markdown('<div class="section-container"><div class="section-header">🎯 Step 2: Who Are You Contacting?</div>', unsafe_allow_html=True)

recipient = st.text_input("**👥 Recipient's Name**", placeholder="e.g., Sarah Chen")

# Smart Research Assistant - Now full width
if recipient:
    st.markdown("### 🔍 Research Assistant (2-3 min for much better results)")
    st.markdown(f"**Quick research for {recipient}:**")
    
    # Research links in a clean row
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={recipient.replace(' ', '%20')}"
        st.markdown(f"[🔗 LinkedIn]({linkedin_url})")
    with col2:
        google_url = f"https://www.google.com/search?q=\"{recipient.replace(' ', '+')}\" recent"
        st.markdown(f"[🔗 Google Recent]({google_url})")
    with col3:
        if st.button("💡 Research Tips"):
            st.session_state.show_tips = not st.session_state.get('show_tips', False)
    
    if st.session_state.get('show_tips', False):
        st.info("""
        **Look for:**
        • Recent LinkedIn posts or job changes
        • Company news they're mentioned in
        • Shared connections or alma mater
        • Recent achievements or projects
        """)
    
    st.markdown("**Fill in what you find (even 1-2 fields help a lot):**")
    
    # Research fields in a better layout
    col1, col2 = st.columns(2)
    with col1:
        company_role = st.text_input("💼 Company & Role", placeholder="e.g., Senior Engineer at Google")
        recent_activity = st.text_input("📈 Recent Achievement/Activity", placeholder="e.g., Published AI research paper")
    
    with col2:
        shared_connection = st.text_input("🤝 Shared Connection", placeholder="e.g., Both worked at Microsoft")
        personal_detail = st.text_input("🎯 Personal Detail", placeholder="e.g., Stanford MBA, loves hiking")
    
    # Auto-combine context with smart formatting
    context_parts = []
    if company_role:
        context_parts.append(f"They work as {company_role}")
    if recent_activity:
        context_parts.append(f"Recently: {recent_activity}")
    if shared_connection:
        context_parts.append(f"Connection: {shared_connection}")
    if personal_detail:
        context_parts.append(f"Background: {personal_detail}")
    
    recipient_context = ". ".join(context_parts)
    
    # Smart feedback
    if len(context_parts) >= 2:
        st.success("✅ Perfect! This will create a highly personalized email")
    elif len(context_parts) == 1:
        st.info("👍 Good start! Adding one more detail will make it even better")
    else:
        st.warning("💡 Adding just 1-2 details above will dramatically improve your email quality")

else:
    st.info("👆 Enter a recipient name above to access research tools")
    recipient_context = ""

# Fallback for manual input
with st.expander("✏️ Or write your own context"):
    manual_context = st.text_area(
        "Manual context about the recipient",
        placeholder="Write anything else you know about them...",
        height=60
    )
    if manual_context:
        recipient_context = manual_context if not recipient_context else f"{recipient_context}. {manual_context}"

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# STEP 3: Message Settings
st.markdown('<div class="section-container"><div class="section-header">⚙️ Step 3: Message Settings</div>', unsafe_allow_html=True)

# Goal and tone in a cleaner layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🎪 What's your goal?**")
    goal_options = ["Ask for a referral", "Request a coffee chat", "Seek resume feedback", "Other (custom)"]
    goal_selection = st.selectbox("", goal_options, label_visibility="collapsed")
    
    if goal_selection == "Other (custom)":
        custom_goal = st.text_input("Custom goal", placeholder="e.g., Discuss collaboration opportunity")
        goal = custom_goal
    else:
        goal = goal_selection

with col2:
    st.markdown("**🎭 Preferred tone?**")
    tone_options = ["Friendly", "Curious", "Professional", "Other (custom)"]
    tone_selection = st.selectbox("", tone_options, label_visibility="collapsed")
    
    if tone_selection == "Other (custom)":
        custom_tone = st.text_input("Custom tone", placeholder="e.g., Enthusiastic, Humble")
        tone = custom_tone
    else:
        tone = tone_selection

# Additional options
st.markdown("**🔧 Additional Options**")
col1, col2 = st.columns(2)

with col1:
    generate_subject = st.checkbox("📧 Generate subject line", value=True)
    
with col2:
    email_length = st.selectbox("Email length:", 
        ["Concise (80-120 words)", "Standard (120-150 words)", "Detailed (150-200 words)"],
        index=1)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Action buttons - Better spacing and layout
st.markdown("### 🚀 Ready to Generate?")

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.user_background = ""
        st.session_state.last_file_id = None
        st.rerun()

with col2:
    generate_button = st.button("✨ Generate Cold Email", use_container_width=True, type="primary")

with col3:
    st.empty()  # For balance

# --- GENERATE ---
if generate_button and user_background and recipient:
    with st.spinner("🤖 Crafting your personalized message..."):
        context_prompt = f"\nAdditional context about the recipient: {recipient_context}" if recipient_context else ""
        
        # Extract word count from email_length selection
        length_mapping = {
            "Concise (80-120 words)": "80-120 words",
            "Standard (120-150 words)": "120-150 words", 
            "Detailed (150-200 words)": "150-200 words"
        }
        word_count = length_mapping[email_length]
        
        prompt = f"""
        You are an expert in professional communication and relationship building. Create a highly personalized cold outreach email that will genuinely connect with the recipient and stand out from generic messages.

        Key requirements:
        - Length: {word_count}
        - Tone: {tone.lower()}
        - Primary goal: {goal}
        {"- Also generate a compelling subject line" if generate_subject else ""}

        Sender's background: {user_background}
        Recipient: {recipient}{context_prompt}

        CRITICAL INSTRUCTIONS:
        1. ONLY use information explicitly provided about the recipient - DO NOT invent or assume details
        2. If minimal context is provided, focus on the sender's value proposition and genuine interest in connecting
        3. If rich context is provided, create specific connections between sender and recipient
        4. Start with a specific, personalized opening that shows you've done your homework (when context allows)
        5. Establish a clear, authentic connection between your background and their work/expertise (when possible)
        6. Be specific about why you chose them (not just anyone in their position) - use provided context only
        7. Make your {goal.lower()} request clear but not demanding
        8. Provide clear value proposition or mutual benefit where appropriate
        9. Keep the focus on quality of connection over asking for favors
        10. Avoid generic phrases like "I hope this email finds you well" or "I would love to pick your brain"
        11. If no specific context is provided, acknowledge this honestly and focus on your genuine interest in their expertise

        {"OUTPUT FORMAT:" if generate_subject else ""}
        {"Subject: [compelling subject line]" if generate_subject else ""}
        {"Email Body: [email content]" if generate_subject else "Write the email body only (no subject line needed)."}
        
        Make it sound natural and conversational, not formulaic.
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
            
            # Parse subject line and email body if subject was generated
            if generate_subject and "Subject:" in result and "Email Body:" in result:
                parts = result.split("Email Body:")
                subject_line = parts[0].replace("Subject:", "").strip()
                email_body = parts[1].strip()
            else:
                subject_line = None
                email_body = result
            
            # Enhanced results display
            st.markdown("---")
            st.markdown("### 🎉 Your Personalized Cold Email")
            
            # Create a nice container for the result
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            
            # Display subject line if generated
            if generate_subject and subject_line:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown("**📧 Subject Line:**")
                with col2:
                    if st.button("📋 Copy Subject", key="copy_subject"):
                        st.success("Subject copied!")
                
                st.text_area("", subject_line, height=50, label_visibility="collapsed", key="subject_display")
                st.markdown("---")
            
            # Display email body
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**To: {recipient}**")
            with col2:
                if st.button("📋 Copy Email", key="copy_email"):
                    st.success("Email copied!")
            
            st.text_area("", email_body, height=200, label_visibility="collapsed", key="email_display")
            
            # Copy all button if subject line exists
            if generate_subject and subject_line:
                if st.button("📋 Copy Subject + Email", use_container_width=True, key="copy_all"):
                    combined_text = f"Subject: {subject_line}\n\n{email_body}"
                    st.success("Complete email copied!")
            
            # Add helpful tips
            with st.expander("💡 Tips for sending your email"):
                st.markdown("""
                - **Best send times**: Tuesday-Thursday, 10 AM - 2 PM typically have better response rates
                - **Follow up**: If no response in 1-2 weeks, send a brief, polite follow-up
                - **LinkedIn**: Consider connecting on LinkedIn after sending the email
                - **Subject line tips**: Keep it under 50 characters, be specific and personal
                - **Mobile preview**: Most emails are read on mobile - keep it concise and scannable
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
            
elif generate_button:
    st.warning("🚨 Please fill in both your background and recipient information to generate an email.")
else:
    st.info("👆 Complete the steps above and click generate to create your personalized cold email!")

