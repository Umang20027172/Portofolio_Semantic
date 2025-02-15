# 📊 Resume Analyzer

A powerful **Streamlit-based Resume Analyzer** that leverages **Google Gemini AI** to provide comprehensive resume analysis. Perfect for recruiters, HR professionals, and job seekers.

## 🌟 Key Features

- 📄 **Resume Upload**: Supports PDF format
- 📝 **Job Description Analysis**: Match resumes against job requirements
- 🔍 **Comprehensive Analysis**:
  - Resume Review
  - Skills Assessment
  - Keyword Optimization
  - ATS Compatibility
  - Match Score Calculation
- 💡 **Custom AI Queries**: Get specific insights about the resume
- 📊 **Interactive UI**: User-friendly interface with real-time analysis

## 🛠️ Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

2. **Set Up Virtual Environment** (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

5. **Run the Application**
```bash
streamlit run main.py
```

## 📁 Project Structure
```
resume-analyzer/
├── main.py              # Main application file
├── requirements.txt     # Project dependencies
├── .env                # Environment variables (create this)
└── README.md           # Project documentation
```

## 🚀 Usage Guide

1. Launch the application
2. Enter the job description in the text area
3. Upload a resume in PDF format
4. Choose from various analysis options:
   - Resume Review
   - Skills Analysis
   - Keyword Analysis
   - Match Score
   - Custom Query
5. View detailed AI-powered analysis and recommendations

## 🎥 Live Demo

Scan the QR code in our presentation to access the live demo!

## 📊 Project Presentation

Check out our detailed presentation (presentation.pdf) which includes:
- Complete project overview
- Technical architecture
- Feature demonstrations
- Live demo QR code
- Future enhancements

## 🔧 Technologies Used

- Python 3.9+
- Streamlit
- Google Gemini AI
- PyMuPDF
- PDF2Image
- Pillow

## 📝 Note

Make sure to:
1. Use your own Google Gemini API key
2. Keep your API key secure
3. Follow rate limits and usage guidelines

## 📈 Future Enhancements

- Multiple resume comparison
- Industry-specific analysis
- Enhanced visualization
- Batch processing
- API integration options

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
