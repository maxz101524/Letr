# NetReach.AI - Cold Email Generator

🚀 **Live Demo**: [Coming Soon - Streamlit Deployment]

Generate personalized cold emails that actually get responses using AI-powered research assistance and proven networking strategies.

## ✨ Features

### 📝 **Smart Profile Building**
- Upload resume for AI-generated professional summary
- Manual profile editing with detailed background input
- Optimized for networking rather than job applications

### 🔍 **Research Assistant**
- Quick research links for LinkedIn and Google searches  
- Structured data collection for recipient context
- Real-time feedback on personalization quality
- Research tips and guidance for better results

### ⚙️ **Customizable Generation**
- Multiple goal types (referrals, coffee chats, advice, custom)
- Tone selection (friendly, professional, curious, custom)
- Email length options (concise, standard, detailed)
- Optional subject line generation

### 🎯 **Enhanced Output**
- Professional email formatting
- Separate subject line and body sections
- Multiple copy options for easy use
- Proven tips for sending and follow-up

### 🤖 **AI-Powered Quality**
- Prevents hallucination of recipient details
- Context-aware personalization
- Length and tone optimization
- Professional networking focus

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/NetReach.git
   cd NetReach/streamlit_MVP_prototype
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

1. **Fork this repository**
2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Set the main file path: `streamlit_MVP_prototype/app.py`

3. **Configure secrets**
   - In Streamlit Cloud dashboard, go to App Settings > Secrets
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "your_openai_api_key_here"
     ```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### App Settings
The app uses GPT-4 for email generation and resume analysis. Ensure your OpenAI account has access to GPT-4 models.

## 📖 How to Use

### Step 1: Your Information
- Upload your resume (PDF) for automatic summary generation, or
- Write your own professional background description
- The more detail you provide, the better the AI can personalize emails

### Step 2: Research Your Recipient  
- Enter the recipient's name
- Use provided research links (LinkedIn, Google) to gather information
- Fill in the structured research fields:
  - Company & Role
  - Recent achievements or activity
  - Shared connections
  - Personal details (education, interests)

### Step 3: Configure Your Message
- Select your goal (referral, coffee chat, advice, etc.)
- Choose your preferred tone
- Pick email length preference  
- Enable/disable subject line generation

### Step 4: Generate & Use
- Click "Generate Cold Email"
- Copy subject line and/or email body
- Send through your preferred email client
- Follow the provided tips for best results

## 🎯 Best Practices

### Research Tips
- Look for recent LinkedIn posts or job changes
- Find mutual connections or shared experiences
- Reference specific projects or achievements
- Note personal interests or background details

### Email Tips
- Send Tuesday-Thursday, 10 AM - 2 PM for best response rates
- Keep subject lines under 50 characters
- Follow up after 1-2 weeks if no response
- Connect on LinkedIn after sending

### Success Factors
- Specific personalization beats generic outreach
- Clear, reasonable asks get better responses
- Value proposition improves response rates
- Professional tone with personal touches works best

## 🛠️ Technical Details

### Built With
- **Streamlit** - Web app framework
- **OpenAI GPT-4** - AI email generation
- **PyMuPDF** - PDF resume processing
- **Python-dotenv** - Environment management

### Architecture
- Single-page Streamlit application
- Stateful session management for user data
- Real-time AI processing with OpenAI API
- Responsive design with custom CSS

### Performance
- Average generation time: 3-5 seconds
- PDF processing: < 2 seconds for typical resumes
- Optimized for mobile and desktop use

## 🔒 Privacy & Security

- No email content is stored or logged
- OpenAI API calls follow their privacy policy
- Environment variables protect API keys
- No personal data persistence beyond session

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

Having issues? Check these common solutions:

### Common Issues
- **"API key not found"**: Ensure OPENAI_API_KEY is set in environment or Streamlit secrets
- **"PDF processing failed"**: Try with a different PDF or manual input
- **"Generation too slow"**: OpenAI API may be experiencing high load

### Contact
- Create an issue in this repository
- Email: [your-email@example.com]
- LinkedIn: [Your LinkedIn Profile]

## 🚧 Roadmap

### v1.1 (Coming Soon)
- Multiple email variations generation
- Email quality scoring system
- Success rate optimization suggestions
- Enhanced mobile experience

### v2.0 (Future)
- ML-powered template optimization
- CRM integrations
- Bulk email generation
- Response tracking analytics

---

**Made with ❤️ for better professional networking** 