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
import streamlit as st
import requests
import pytesseract
import pypdfium2
from PIL import Image
import io

st.header("Bank BABA")

uploaded_file = st.file_uploader("Upload Your Bank Statement (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

extracted_text = None

if uploaded_file:
    st.info("Processing uploaded file...")
    
    if uploaded_file.type == "application/pdf":
        # Read PDF file
        pdf_reader = pypdfium2.PdfDocument(io.BytesIO(uploaded_file.read()))
        
        # Render pages as images
        images = []
        for i in range(len(pdf_reader)):
            page = pdf_reader[i]  # Get page
            bitmap = page.render(scale=2.0)  # Render page to bitmap
            img = bitmap.to_pil()  # Convert bitmap to PIL image
            images.append(img)

        # Extract text using OCR
        extracted_text = " ".join(pytesseract.image_to_string(img) for img in images)

    else:
        image = Image.open(uploaded_file)
        extracted_text = pytesseract.image_to_string(image)

    # Display extracted text
    if extracted_text:
        st.subheader("Extracted Text from Bank Statement")
        st.text_area("OCR Result", extracted_text, height=200)
