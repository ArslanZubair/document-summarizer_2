import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai

# ---- Page Configuration ----
st.set_page_config(page_title="AI Document Summarizer", page_icon="📄", layout="wide")

# ---- Custom CSS for Styling ----
st.markdown("""
    <style>
        .big-title { 
            font-size: 38px; 
            font-weight: bold; 
            color: white; 
            text-align: center; 
            line-height: 1.3;
        }
        .small-text { 
            font-size: 16px; 
            color: #ccc; 
            text-align: center;
        }
        .stTextArea textarea { 
            border-radius: 10px; 
            padding: 10px; 
        
        }
        .stButton button { 
            background-color: #4CAF50; 
            color: white; 
            font-weight: bold; 
            border-radius: 8px; 
            padding: 8px 15px;
        }
        .response-box { 
            padding: 15px; 
            border-radius: 10px; 
            font-size: 18px;
        }
        .centered { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ---- Title Section ----
st.markdown('<h1 class="big-title">📄 AI Document <br> Summarizer Tool</h1>', unsafe_allow_html=True)
st.markdown('<p class="small-text">Turn your documents into concise, insightful summaries with AI-powered analysis.✨</p>', unsafe_allow_html=True)

# ---- Retrieve API key ----
# api_key = st.secrets["google_ai"]["api_key"]

# Configure Google Gemini AI
genai.configure(api_key="AIzaSyDxDy4AeLZ3086lATfUTuqSQ_95cdtENj0")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# ---- Function to extract text from PDF ----
def extract_text_from_pdf(pdf_file):
    pdf_bytes = pdf_file.getvalue()
    doc = fitz.open("pdf", pdf_bytes)
    text = "\n".join(page.get_text("text") for page in doc)
    return text

# ---- Initialize session state for question reset ----
if "prev_uploaded_file" not in st.session_state:
    st.session_state.prev_uploaded_file = None
if "question_text" not in st.session_state:
    st.session_state.question_text = ""

# ---- File uploader ----
st.subheader("📤 Upload a Document")
uploaded_file = st.file_uploader("Upload a document(.pdf, .txt, .md)", type=("pdf", "txt", "md"))

# Reset the question box when a new file is uploaded
if uploaded_file and uploaded_file != st.session_state.prev_uploaded_file:
    st.session_state.question_text = ""  
    st.session_state.prev_uploaded_file = uploaded_file  

document_text = ""
if uploaded_file:
    file_type = uploaded_file.type
    with st.spinner("🔄 Extracting text from document..."):
        if file_type == "application/pdf":
            document_text = extract_text_from_pdf(uploaded_file)
        else:
            document_text = uploaded_file.getvalue().decode()

# ---- Ask for user question ----
st.subheader("📝 Ask a Question")
question = st.text_area("Now ask a question about the document!", 
                        placeholder="Can you give me a short summary?", 
                        disabled=not document_text,
                        key="question_text")  

# ---- Generate response ----
if document_text and question:
    if st.button("🔍 Generate Summary"):
        with st.spinner("🤖 AI is thinking..."):
            messages = [{"parts": [{"text": f"Here's a document: {document_text} \n\n---\n\n {question}"}]}]
            response = model.generate_content(messages)

        # ---- Display AI response ----
        st.subheader("📢 AI Response")
        st.markdown(f'<div class="response-box">{response.text}</div>', unsafe_allow_html=True)
