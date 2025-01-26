import streamlit as st
from langchain_ollama import ChatOllama
import PyPDF2

# Set dark theme and wide layout
st.set_page_config(
    page_title="Chat App with Dark Mode",
    layout="wide",  # Expands the canvas to a wide layout
    initial_sidebar_state="collapsed",
)

# Apply dark theme through custom CSS
st.markdown(
    """
    <style>
        /* Force dark theme */
        body {
            background-color: #0e1117;
            color: #f0f0f0;
        }
        .stButton button {
            background-color: #3b3b3b;
            color: white;
            border-radius: 5px;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;  /* Change background color to white */
            color: #0e1117;  /* Change text color to dark */
            border: 1px solid #555555;
        }
        .block-container {
            padding: 2rem 3rem;  /* Increase padding to improve spacing */
        }
        .css-1d391kg {
            max-width: 95%;  /* Adjust the app width to fit most screens */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 PDF Chat Assistant !!!")


def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text()
    return extracted_text


def generate_response(input_text):
    """Generate a response using the ChatOllama model."""
    model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434/")
    response = model.invoke(input_text)
    return response.content


# File upload section
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF processed successfully!")

    with st.form("pdf-llm-form"):
        query = st.text_input("Ask a question or summarize the PDF content:")
        submit_pdf = st.form_submit_button("Submit")

    if submit_pdf and query:
        with st.spinner("Generating response..."):
            combined_input = f"{pdf_text}\n\n{query}"
            response = generate_response(combined_input)
            st.write("## Response")
            st.write(response)
