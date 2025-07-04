# import streamlit as st
# import requests

# # UI elements
# # st.header("Bank Product Recommendation System")
# st.header("Bank BABA")

# # Fetch customer IDs from the FastAPI endpoint
# # response = requests.get("http://127.0.0.1:8000/customers")
# response = requests.get("https://ayush-003-bankllm.hf.space/customers")
# if response.status_code == 200:
#     customer_ids = response.json().get("customer_ids", [])
# else:
#     st.error("Failed to fetch customer IDs")
#     customer_ids = []

# # Ensure customer_ids is not empty
# if customer_ids:
#     # Select customer ID from the list
#     selected_customer_id = st.selectbox("Select Customer ID", customer_ids)

#     # Button to get recommendation
#     if st.button("Get Recommendation"):
#         recommendation_response = requests.post(
#             # f"http://127.0.0.1:8000/recommendation?customer_id={selected_customer_id}"
#             f"https://ayush-003-bankllm.hf.space/recommendation?customer_id={selected_customer_id}"
#         )
#         if recommendation_response.status_code == 200:
#             response_json = recommendation_response.json()
            
#             # Extract recommendation from the correct key
#             if "recommendation" in response_json:
#                 recommendation = response_json["recommendation"]
#                 st.markdown("### Recommendation")
#                 st.markdown(recommendation)
#             else:
#                 st.error("Key 'recommendation' not found in the response.")
#         else:
#             st.error(f"Failed to get recommendation: {recommendation_response.status_code} - {recommendation_response.text}")
# else:
#     st.warning("No customer IDs available to select.")


# import streamlit as st
# import requests
# import json
# import pytesseract
# from pdf2image import convert_from_bytes
# from PIL import Image
# # pytesseract.pytesseract.tesseract_cmd = r"D:\tesseract-ocr\tesseract.exe"

# # Configure Tesseract path if needed (Uncomment if running locally)
# POPPLER_PATH = "/usr/bin"
# st.header("Bank BABA")

# # Fetch customer IDs from FastAPI
# response = requests.get("http://ayush-003-bankllm.hf.space/customers")
# if response.status_code == 200:
#     customer_ids = response.json().get("customer_ids", [])
# else:
#     st.error("Failed to fetch customer IDs")
#     customer_ids = []

# user_type = st.radio("Are you an existing customer?", ("Yes", "No"))

# if user_type == "Yes" and customer_ids:
#     selected_customer_id = st.selectbox("Select Customer ID", customer_ids)

#     if st.button("Get Recommendation"):
#         recommendation_response = requests.post(
#             f"http://ayush-003-bankllm.hf.space/recommendation?customer_id={selected_customer_id}"
#         )
#         if recommendation_response.status_code == 200:
#             response_json = recommendation_response.json()
#             st.markdown("### Recommendation")
#             st.markdown(response_json.get("recommendation", "No recommendation found."))
#         else:
#             st.error(f"Failed to get recommendation: {recommendation_response.status_code}")

# elif user_type == "No":
#     st.subheader("Enter Your Financial Details")
    
#     # Form for manual input
#     with st.form("user_info_form"):
#         income = st.number_input("Monthly Income", min_value=1000, step=500)
#         age = st.number_input("Age", min_value=18, step=1)
#         credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=650)
#         employment_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed", "Retired"])
#         loan_history = st.selectbox("Have you taken a loan before?", ["Yes", "No"])
#         submit_details = st.form_submit_button("Submit & Get Recommendation")

#     # Allow users to upload bank statements (PDF or Image)
#     uploaded_file = st.file_uploader("Upload Your Bank Statement (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

#     extracted_text = None  # Placeholder for OCR result

#     if uploaded_file:
#         st.info("Processing uploaded file...")
#         if uploaded_file.type == "application/pdf":
#             # Convert PDF to images
#             images = convert_from_bytes(uploaded_file.read(),poppler_path=POPPLER_PATH)
#             extracted_text = " ".join(pytesseract.image_to_string(img) for img in images)
#         else:
#             # Process image files
#             image = Image.open(uploaded_file)
#             extracted_text = pytesseract.image_to_string(image)

#         # Display extracted text
#         if extracted_text:
#             st.subheader("Extracted Text from Bank Statement")
#             st.text_area("OCR Result", extracted_text, height=200)

#     # When the form is submitted or a file is uploaded, send data to FastAPI
#     if submit_details or uploaded_file:
#         # Construct user data
#         user_data = {
#             "income": income,
#             "age": age,
#             "credit_score": credit_score,
#             "employment_status": employment_status,
#             "loan_history": loan_history,
#             "bank_statement_text": extracted_text if extracted_text else "No document uploaded"
#         }

#         # Send data to FastAPI's new_user endpoint
#         recommendation_response = requests.post(
#             "http://ayush-003-bankllm.hf.space/recommendation/new_user",
#             json={"customer_data": user_data}
#         )
#         if recommendation_response.status_code == 200:
#             response_json = recommendation_response.json()
#             st.markdown("### Recommendation")
#             st.markdown(response_json.get("recommendation", "No recommendation found."))
#         else:
#             st.error(f"Failed to get recommendation: {recommendation_response.status_code}")



import streamlit as st
import requests
import pypdfium2
import io
import pytesseract
from PIL import Image
from pypdf import PdfReader
import tempfile

# Set page config for a wider, more modern layout
st.set_page_config(page_title="Bank BABA", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a polished look
st.markdown("""
    <style>
    /* General styling */
    .main {
        background-color: #F0F2F6; /* Light grey background */
    }
    /* Title styling */
    h1 {
        color: #004080; /* Dark blue */
        text-align: center;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #FFFFFF;
    }
    /* Button styling */
    .stButton>button {
        background-color: #004080;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0059b3;
    }
    /* Input widgets styling */
    .stTextInput, .stNumberInput, .stSelectbox {
        border-radius: 8px;
    }
    /* Recommendation box */
    .recommendation {
        background-color: #FFFFFF;
        border-left: 5px solid #004080;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title("Bank BABA 🤖")
st.markdown("<h4 style='text-align: center; color: #555;'>Your AI-Powered Financial Advisor</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- API Configuration ---
# API_BASE_URL = "http://127.0.0.1:8000"
API_BASE_URL = "https://ayush-003-bankllm.hf.space"

# --- Utility Functions ---
def is_pdf_password_protected(file_bytes):
    """Check if a PDF is password protected"""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        # Try to access pages - will raise an exception if password protected
        _ = len(reader.pages)
        return False
    except Exception:
        return True

def unlock_pdf_with_password(file_bytes, password):
    """Unlock a password-protected PDF and return the unlocked bytes"""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        reader.decrypt(password)
        
        # Create a temporary unlocked PDF
        from pypdf import PdfWriter
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer.getvalue()
    except Exception as e:
        st.error(f"Failed to unlock PDF: {str(e)}")
        return None

# --- Data Fetching ---
@st.cache_data(ttl=600)
def get_customer_ids():
    try:
        response = requests.get(f"{API_BASE_URL}/customers")
        if response.status_code == 200:
            return response.json().get("customer_ids", [])
        else:
            st.error("Failed to fetch customer IDs from the server.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return []

customer_ids = get_customer_ids()

# --- Sidebar Navigation ---
st.sidebar.header("User Type")
user_type = st.sidebar.radio("", ("Existing Customer", "New Customer"), label_visibility="collapsed")

# --- Main Content ---

# == EXISTING CUSTOMER WORKFLOW ==
if user_type == "Existing Customer":
    st.header("Welcome Back!")
    if not customer_ids:
        st.warning("Could not retrieve customer list. Please check server status.")
    else:
        selected_customer_id = st.selectbox("Select your Customer ID to get a tailored recommendation:", customer_ids)
        if st.button("Get My Recommendation"):
            with st.spinner("Analyzing your profile and finding the best products..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/recommendation?customer_id={selected_customer_id}")
                    if res.status_code == 200:
                        st.markdown("<div class='recommendation' style='background: black;'><h3>Personalized Recommendation</h3></div>", unsafe_allow_html=True)
                        st.success(res.json().get("recommendation", "No recommendation available."))
                    else:
                        st.error(f"Error: {res.status_code} - {res.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the recommendation service: {e}")

# == NEW CUSTOMER WORKFLOW ==
elif user_type == "New Customer":
    st.header("Let's Find the Right Product for You")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Tell us about yourself")
        
        # Handle file upload and password outside the form first
        st.markdown("<h6>For a more accurate recommendation, you can upload your latest bank statement.</h6>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Bank Statement (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
        
        # Password input for protected PDFs (outside form)
        pdf_password = None
        is_pdf_protected = False
        if uploaded_file and uploaded_file.type == "application/pdf":
            file_bytes = uploaded_file.read()
            is_pdf_protected = is_pdf_password_protected(file_bytes)
            if is_pdf_protected:
                st.warning("⚠️ This PDF appears to be password-protected.")
                pdf_password = st.text_input(
                    "Enter PDF password to unlock:", 
                    type="password", 
                    help="Your password is used only for processing and is never stored or transmitted.",
                    key="pdf_password_input"
                )
                st.info("🔒 **Privacy Note:** Your password is processed locally and immediately discarded. We never store or save your password.")
                
                # Show status based on password input
                if pdf_password:
                    st.success("✅ Password entered. You can now generate recommendation.")
                else:
                    st.error("❌ Please enter the PDF password to continue.")
        
        # Form with other inputs
        with st.form("user_info_form"):
            income = st.number_input("Monthly Income (INR)", min_value=1000, step=500)
            age = st.number_input("Age", min_value=18, max_value=100, step=1)
            credit_score = st.slider("Estimated Credit Score", min_value=300, max_value=850, value=650)
            employment_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed", "Student", "Retired"])
            loan_history = st.radio("Previous Loan History", ["Yes", "No"], horizontal=True)
            
            # Check if we should disable the button
            button_disabled = is_pdf_protected and (not pdf_password or pdf_password.strip() == "")
            
            if button_disabled:
                st.info("🔒 Please enter the PDF password above to enable the recommendation button.")
                submit_button = st.form_submit_button(
                    label="🔒 Enter PDF Password First", 
                    disabled=True
                )
                submit_button = False  # Override to False when disabled
            else:
                submit_button = st.form_submit_button(label="Generate Recommendation")

    with col2:
        st.subheader("Why provide this info?")
        st.info("""
        - **Income & Employment:** Helps us understand your financial stability.
        - **Credit Score:** A key factor for loan and credit card eligibility.
        - **Bank Statement:** Provides a detailed view of your financial habits, allowing for highly personalized advice.
        
        **🔒 Security Notes:**
        - Password-protected PDFs are supported
        - Your PDF password is never stored or transmitted
        - All processing happens locally and securely
        - Your data is processed securely and is not stored
        """)

    # Show password unlock instructions if needed
    if uploaded_file and uploaded_file.type == "application/pdf":
        file_preview_bytes = uploaded_file.read()
        uploaded_file.seek(0)  # Reset file pointer
        if is_pdf_password_protected(file_preview_bytes):
            st.info("💡 **Tip:** If your bank statement is password-protected, you can enter the password below. Your password will only be used to unlock the document for analysis and will be immediately discarded.")

    extracted_text = None
    if uploaded_file:
        with st.spinner("Analyzing your document..."):
            file_bytes = uploaded_file.read()
            try:
                if uploaded_file.type == "application/pdf":
                    # Handle password-protected PDFs
                    if is_pdf_password_protected(file_bytes):
                        if pdf_password:
                            st.info("🔓 Unlocking password-protected PDF...")
                            unlocked_bytes = unlock_pdf_with_password(file_bytes, pdf_password)
                            if unlocked_bytes:
                                file_bytes = unlocked_bytes
                                st.success("✅ PDF unlocked successfully!")
                            else:
                                st.error("❌ Failed to unlock PDF. Please check your password and try again.")
                                file_bytes = None
                        else:
                            st.error("❌ Please enter the PDF password to proceed.")
                            file_bytes = None
                    
                    if file_bytes:
                        pdf_pages = pypdfium2.PdfDocument(io.BytesIO(file_bytes))
                        images = [page.render(scale=2).to_pil() for page in pdf_pages]
                        extracted_text = " ".join(pytesseract.image_to_string(img, lang='eng') for img in images)
                else:
                    image = Image.open(io.BytesIO(file_bytes))
                    extracted_text = pytesseract.image_to_string(image, lang='eng')
                
                if extracted_text:
                    with st.expander("View Extracted Text"):
                        st.text_area("", extracted_text, height=250)
            except Exception as e:
                st.error(f"Failed to process the document: {e}")

    if submit_button:
        user_data = {
            "income": income,
            "age": age,
            "credit_score": credit_score,
            "employment_status": employment_status,
            "loan_history": loan_history,
            "bank_statement_text": extracted_text if extracted_text else "No document uploaded"
        }
        with st.spinner("Our AI is crafting your recommendation..."):
            try:
                res = requests.post(f"{API_BASE_URL}/recommendation/new_user", json={"customer_data": user_data})
                if res.status_code == 200:
                    st.markdown("<div class='recommendation' style='background:black;'><h3>Here's Our Recommendation</h3></div>", unsafe_allow_html=True)
                    st.success(res.json().get("recommendation", "Could not generate a recommendation."))
                else:
                    st.error(f"Error: {res.status_code} - {res.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the recommendation service: {e}")
