


Resume Analyzer
Overview
Resume Analyzer is an advanced web application built with Streamlit that helps users analyze resumes against job descriptions using Google's Gemini AI. This tool streamlines the resume review process by providing detailed analysis, skills assessment, and job matching capabilities.
Features

Resume Review: Comprehensive evaluation of resumes against job descriptions
Skills Analysis: Detailed assessment of technical and professional skills
Keyword Analysis: ATS-friendly keyword optimization suggestions
Match Score: Calculate compatibility between resume and job requirements
Custom Queries: Flexibility to ask specific questions about the resume

Technologies Used

Python
Streamlit
Google Gemini AI
PyMuPDF (fitz)
PIL (Python Imaging Library)
PDF2Image

Prerequisites
To run this application, you need:

Python 3.7+
Google Gemini AI API key

Installation

Clone the repository:

bashCopygit clone <repository-url>
cd resume-analyzer

Install required dependencies:

bashCopypip install -r requirements.txt

Set up your Google Gemini AI API key:

Option 1: Replace the API key directly in the code
Option 2: Use Streamlit secrets management



Usage

Start the application:

bashCopystreamlit run app.py

Access the web interface through your browser
Upload a resume (PDF format)
Enter the job description
Choose from various analysis options:

Resume Review
Skills Analysis
Keyword Analysis
Match Score
Custom Query
