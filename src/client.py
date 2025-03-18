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
# from pdf2image import convert_from_bytes
from PIL import Image
import subprocess
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

st.header("Bank BABA")
try:
    result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
    st.text(f"Tesseract Version: {result.stdout}")
except FileNotFoundError:
    st.error("Tesseract is not installed. Ensure it's available in the deployment environment.")

response = requests.get("https://ayush-003-bankllm.hf.space/customers")
# response = requests.get("http://127.0.0.1:8000/customers")
if response.status_code == 200:
    customer_ids = response.json().get("customer_ids", [])
else:
    st.error("Failed to fetch customer IDs")
    customer_ids = []

user_type = st.radio("Are you an existing customer?", ("Yes", "No"))

if user_type == "Yes" and customer_ids:
    selected_customer_id = st.selectbox("Select Customer ID", customer_ids)

    if st.button("Get Recommendation"):
        recommendation_response = requests.post(
            # f"http://127.0.0.1:8000/recommendation?customer_id={selected_customer_id}"
            f"https://ayush-003-bankllm.hf.space/recommendation?customer_id={selected_customer_id}"
        )
        if recommendation_response.status_code == 200:
            response_json = recommendation_response.json()
            st.markdown("### Recommendation")
            st.markdown(response_json.get("recommendation", "No recommendation found."))
        else:
            st.error(f"Failed to get recommendation: {recommendation_response.status_code}")

elif user_type == "No":
    st.subheader("Enter Your Financial Details")
   
    with st.form("user_info_form"):
        income = st.number_input("Monthly Income", min_value=1000, step=500)
        age = st.number_input("Age", min_value=18, step=1)
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=650)
        employment_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed", "Retired"])
        loan_history = st.selectbox("Have you taken a loan before?", ["Yes", "No"])
        submit_details = st.form_submit_button("Submit & Get Recommendation")
    uploaded_file = st.file_uploader("Upload Your Bank Statement (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

    extracted_text = None  # Placeholder for OCR result

    if uploaded_file:
        st.info("Processing uploaded file...")
        file_bytes = uploaded_file.read()
        if uploaded_file.type == "application/pdf":
            pdf_reader = pypdfium2.PdfDocument(io.BytesIO(file_bytes))
            images=[]
            for i in range(len(pdf_reader)):
                page=pdf_reader[i]
                bitmap=page.render(scale=2.0)
                img=bitmap.to_pil()
                images.append(img)
            extracted_text = " ".join(pytesseract.image_to_string(img,lang='eng') for img in images)
        else:
            image=Image.open(io.BytesIO(file_bytes))
            extracted_text = pytesseract.image_to_string(image,lang='eng')
        if extracted_text:
            st.subheader("Extracted Text from Bank Statement")
            st.text_area("OCR Result", extracted_text, height=200)
  
    if submit_details or uploaded_file:
       
        user_data = {
            "income": income,
            "age": age,
            "credit_score": credit_score,
            "employment_status": employment_status,
            "loan_history": loan_history,
            "bank_statement_text": extracted_text if extracted_text else "No document uploaded"
        }

        # Send data to FastAPI's new_user endpoint
        recommendation_response = requests.post(
            "https://ayush-003-bankllm.hf.space/recommendation/new_user",
            # "http://127.0.0.1:8000/recommendation/new_user",
            json={"customer_data": user_data}
        )
        if recommendation_response.status_code == 200:
            response_json = recommendation_response.json()
            st.markdown("### Recommendation")
            st.markdown(response_json.get("recommendation", "No recommendation found."))
        else:
            st.error(f"Failed to get recommendation: {recommendation_response.status_code}")
