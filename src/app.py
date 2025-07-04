# import logging
# from fastapi import FastAPI, HTTPException
# from langchain.prompts import PromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI 
# from langchain.chains import SequentialChain, LLMChain
# from langchain_community.vectorstores import FAISS
# from langchain.docstore.document import Document
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from config import *
# from db_connect import fetch_data_as_json
# import json
# import os

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# # Set environment variables for Langchain 
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# # Initialize FastAPI app
# app = FastAPI(
#     title="Bank Product Recommendation System",
#     version="1.0",
#     description="API for generating bank product recommendations using LangChain"
# )

# # Load customer data from MySQL with error handling
# try:
#     logger.info("Fetching customer data from MySQL...")
#     customer_data_loaded = fetch_data_as_json("CustomerProfile", "customer_profile.json")
#     with open("customer_profile.json", 'r') as json_file:
#         customer_dataset = json.load(json_file)
#     logger.info(f"✅ Loaded {len(customer_dataset)} customer records.")
# except Exception as e:
#     logger.error(f"❌ Error fetching customer data: {e}")
#     customer_dataset = []

# # Load product data from MySQL with error handling
# try:
#     logger.info("Fetching product data from MySQL...")
#     product_data_loaded = fetch_data_as_json("Products", "products.json")
#     with open("products.json", 'r') as json_file:
#         product_dataset = json.load(json_file)
#     logger.info(f"✅ Loaded {len(product_dataset)} product records.")
# except Exception as e:
#     logger.error(f"❌ Error fetching product data: {e}")
#     product_dataset = []

# # Initialize vector store and other LangChain components
# documents = []
# try:
#     logger.info("Initializing FAISS Vector Store...")
#     for customer in customer_dataset:
#         documents.append(Document(page_content=json.dumps(customer, indent=4), metadata={"class": customer["CustomerID"]}))
    
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     db = FAISS.from_documents(documents, embeddings)
#     logger.info("✅ FAISS Vector Store initialized successfully.")

# except Exception as e:
#     logger.error(f"❌ Error initializing FAISS: {e}")
#     db = None  # Prevent API crash if FAISS fails

# # Define prompts
# first_template = """
# You are a professional data analyst at a bank. You have been provided with detailed customer information.
# Analyze the following customer data and provide insights into their financial needs, potential risks, and opportunities for product offerings.
# Customer Information: {query}
# Analysis:
# """

# second_template = """
# As a professional financial advisor at a bank, your goal is to provide tailored recommendations that align with the customer's financial situation and goals.
# Using the customer analysis provided and the available banking products, determine the most suitable product(s) for this customer.
# Please explain why this product is the best fit, considering the customer's financial needs, potential risks, and long-term benefits.
# Customer Analysis: {customer_analysis}
# Available Products: {product_info}
# Recommendation:
# """

# # Initialize model and prompts
# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )

# first_prompt = PromptTemplate(input_variables=["query"], template=first_template)
# second_prompt = PromptTemplate(input_variables=["customer_analysis", "product_info"], template=second_template)

# # Combine both chains into a SequentialChain
# first_chain = LLMChain(llm=model, prompt=first_prompt, output_key="customer_analysis", verbose=True)
# second_chain = LLMChain(llm=model, prompt=second_prompt, output_key="final_recommendation", verbose=True)

# sequential_chain = SequentialChain(
#     chains=[first_chain, second_chain],
#     input_variables=["query", "product_info"],
#     output_variables=["final_recommendation"]
# )

# # Define the route to get all customer IDs
# @app.get("/customers")
# async def get_customer_ids():
#     if not customer_dataset:
#         raise HTTPException(status_code=500, detail="Customer data not available")
    
#     customer_ids = [customer["CustomerID"] for customer in customer_dataset]
#     return {"customer_ids": customer_ids}

# # Define the route to generate recommendations
# @app.post("/recommendation")
# async def generate_recommendation(customer_id: str):
#     if db is None:
#         raise HTTPException(status_code=500, detail="Vector database not initialized")
    
#     retriever = db.as_retriever(search_kwargs={"k": 1})
#     retrieved_documents = retriever.get_relevant_documents(customer_id)
    
#     if not retrieved_documents:
#         logger.warning(f"Customer ID {customer_id} not found in FAISS.")
#         raise HTTPException(status_code=404, detail="Customer not found")
    
#     customer_info = "\n".join([doc.page_content for doc in retrieved_documents])
    
#     product_info = "\n".join(
#         [f"Name: {prod['name']}, Category: {prod['category']}, Features: {prod['features']}, Description: {prod['description']}" 
#         for prod in product_dataset]
#     )
    
#     logger.info(f"Generating recommendation for Customer ID: {customer_id}")
#     result = sequential_chain({"query": customer_info, "product_info": product_info})
    
#     return {"recommendation": result["final_recommendation"]}

# if __name__ == "__main__":
#     import uvicorn
#     logger.info("🚀 Starting FastAPI server on port 8000...")
#     uvicorn.run(app, host="0.0.0.0", port=8000)
import logging
import json
import os
from fastapi import FastAPI, HTTPException, status
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import SequentialChain, LLMChain
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import BaseModel

# Local imports
from config import LANGCHAIN_API_KEY
from db_connect import fetch_data_as_json

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- Environment Variables ---
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Bank Product Recommendation API",
    version="2.0",
    description="An AI-powered API for recommending bank products to new and existing customers.",
)

# --- Data Models ---
class CustomerData(BaseModel):
    income: float
    age: int
    credit_score: int
    employment_status: str
    loan_history: str
    bank_statement_text: str | None = None

class NewUserRequest(BaseModel):
    customer_data: CustomerData

# --- Global Variables & Data Loading ---
customer_dataset = []
product_dataset = []
db = None

@app.on_event("startup")
async def startup_event():
    global customer_dataset, product_dataset, db
    # Load customer data
    try:
        logger.info("Fetching customer data from MySQL...")
        if fetch_data_as_json("CustomerProfile", "customer_profile.json"):
            with open("customer_profile.json", 'r') as f:
                customer_dataset = json.load(f)
            logger.info(f"✅ Loaded {len(customer_dataset)} customer records.")
        else:
            logger.warning("Could not fetch or write customer data.")
    except Exception as e:
        logger.error(f"❌ Failed to load customer data: {e}")

    # Load product data
    try:
        logger.info("Fetching product data from MySQL...")
        if fetch_data_as_json("Products", "products.json"):
            with open("products.json", 'r') as f:
                product_dataset = json.load(f)
            logger.info(f"✅ Loaded {len(product_dataset)} product records.")
        else:
            logger.warning("Could not fetch or write product data.")
    except Exception as e:
        logger.error(f"❌ Failed to load product data: {e}")

    # Initialize FAISS Vector Store
    if customer_dataset:
        try:
            logger.info("Initializing FAISS Vector Store...")
            documents = [
                Document(page_content=json.dumps(customer, indent=4), metadata={"class": customer["CustomerID"]})
                for customer in customer_dataset
            ]
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            db = FAISS.from_documents(documents, embeddings)
            logger.info("✅ FAISS Vector Store initialized successfully.")
        except Exception as e:
            logger.error(f"❌ Error initializing FAISS: {e}")

# --- LLM and Chains Configuration ---
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2, max_tokens=2048)

# Templates for Existing Customers
analysis_template = """
Role: You are a professional bank data analyst.
Task: Analyze the provided customer JSON data. Summarize their financial profile, identify key needs, potential risks, and opportunities for new banking products.
Customer Data:
{query}
---
Analysis Output:
"""
recommendation_template = """
Role: You are an expert financial advisor.
Task: Based on the customer analysis and the list of available bank products, provide a tailored recommendation.
Explain clearly why the chosen product(s) are a good fit for the customer's needs and financial situation.
Format your output clearly. Start with the recommended product name, followed by the justification.

Customer Analysis:
{customer_analysis}

Available Products:
{product_info}
---
Final Recommendation:
"""

# Chains for Existing Customers
analysis_prompt = PromptTemplate(input_variables=["query"], template=analysis_template)
analysis_chain = LLMChain(llm=llm, prompt=analysis_prompt, output_key="customer_analysis")

recommendation_prompt = PromptTemplate(input_variables=["customer_analysis", "product_info"], template=recommendation_template)
recommendation_chain = LLMChain(llm=llm, prompt=recommendation_prompt, output_key="final_recommendation")

existing_customer_chain = SequentialChain(
    chains=[analysis_chain, recommendation_chain],
    input_variables=["query", "product_info"],
    output_variables=["final_recommendation"],
    verbose=True,
)

# Templates for New Customers
new_user_analysis_template = """
Role: You are a sharp financial analyst at a leading bank.
Task: A prospective customer has provided their financial details. Analyze this information, including any text from their bank statement, to create a concise financial summary.
Identify their potential financial needs (e.g., savings, credit, investment) and assess their financial health.

Customer Details:
{query}
---
Financial Summary:
"""
new_user_recommendation_template = """
Role: You are a friendly and professional bank advisor.
Task: Based on the financial summary of the prospective customer and the bank's product catalog, recommend the most suitable product(s).
Explain your recommendation in a simple, compelling way. Highlight the benefits for the customer.

Financial Summary:
{customer_analysis}

Available Products:
{product_info}
---
New Customer Recommendation:
"""

# Chains for New Customers
new_user_analysis_prompt = PromptTemplate(input_variables=["query"], template=new_user_analysis_template)
new_user_analysis_chain = LLMChain(llm=llm, prompt=new_user_analysis_prompt, output_key="customer_analysis")

new_user_recommendation_prompt = PromptTemplate(input_variables=["customer_analysis", "product_info"], template=new_user_recommendation_template)
new_user_recommendation_chain = LLMChain(llm=llm, prompt=new_user_recommendation_prompt, output_key="final_recommendation")

new_customer_chain = SequentialChain(
    chains=[new_user_analysis_chain, new_user_recommendation_chain],
    input_variables=["query", "product_info"],
    output_variables=["final_recommendation"],
    verbose=True,
)

# --- Helper Functions ---
def get_product_info_string():
    if not product_dataset:
        return "No product information available."
    return "\n".join(
        [f"- Name: {p['name']}, Category: {p['category']}, Features: {p['features']}" for p in product_dataset]
    )

# --- API Endpoints ---
@app.get("/customers")
async def get_all_customer_ids():
    """Returns a list of all available customer IDs."""
    if not customer_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer data not available.")
    return {"customer_ids": [c["CustomerID"] for c in customer_dataset]}

@app.post("/recommendation")
async def generate_recommendation(customer_id: str):
    """Generates a product recommendation for an existing customer."""
    if db is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Vector database is not initialized.")
    
    retriever = db.as_retriever(search_kwargs={"k": 1})
    docs = retriever.get_relevant_documents(customer_id)
    
    if not docs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID '{customer_id}' not found.")
        
    customer_info = docs[0].page_content
    product_info = get_product_info_string()
    
    logger.info(f"Generating recommendation for existing customer: {customer_id}")
    result = await existing_customer_chain.ainvoke({"query": customer_info, "product_info": product_info})
    
    return {"recommendation": result["final_recommendation"]}

@app.post("/recommendation/new_user")
async def generate_new_user_recommendation(request: NewUserRequest):
    """Generates a product recommendation for a new, prospective customer."""
    if not product_dataset:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Product data is not available.")

    customer_info = json.dumps(request.customer_data.dict(), indent=4)
    product_info = get_product_info_string()

    logger.info("Generating recommendation for a new user.")
    try:
        result = await new_customer_chain.ainvoke({"query": customer_info, "product_info": product_info})
        return {"recommendation": result["final_recommendation"]}
    except Exception as e:
        logger.error(f"❌ Error during new user recommendation generation: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate recommendation.")

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting FastAPI server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
