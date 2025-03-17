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
from fastapi import FastAPI, HTTPException
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.chains import SequentialChain, LLMChain
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import LANGCHAIN_API_KEY
from db_connect import fetch_data_as_json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Set environment variables for LangChain
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# Initialize FastAPI app
app = FastAPI(
    title="Bank Product Recommendation System",
    version="1.0",
    description="API for generating bank product recommendations using LangChain"
)

# Load customer data from MySQL with error handling
try:
    logger.info("Fetching customer data from MySQL...")
    fetch_data_as_json("CustomerProfile", "customer_profile.json")
    with open("customer_profile.json", 'r') as json_file:
        customer_dataset = json.load(json_file)
    logger.info(f"✅ Loaded {len(customer_dataset)} customer records.")
except Exception as e:
    logger.error(f"❌ Error fetching customer data: {e}")
    customer_dataset = []

# Load product data from MySQL with error handling
try:
    logger.info("Fetching product data from MySQL...")
    fetch_data_as_json("Products", "products.json")
    with open("products.json", 'r') as json_file:
        product_dataset = json.load(json_file)
    logger.info(f"✅ Loaded {len(product_dataset)} product records.")
except Exception as e:
    logger.error(f"❌ Error fetching product data: {e}")
    product_dataset = []

# Initialize FAISS Vector Store with customer documents
documents = []
try:
    logger.info("Initializing FAISS Vector Store...")
    for customer in customer_dataset:
        documents.append(Document(page_content=json.dumps(customer, indent=4),
                                  metadata={"class": customer["CustomerID"]}))
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(documents, embeddings)
    logger.info("✅ FAISS Vector Store initialized successfully.")
except Exception as e:
    logger.error(f"❌ Error initializing FAISS: {e}")
    db = None  # Prevent API crash if FAISS fails

# Define common prompt templates for existing customers
first_template = """
You are a professional data analyst at a bank. You have been provided with detailed customer information.
Analyze the following customer data and provide insights into their financial needs, potential risks, and opportunities for product offerings.
Customer Information: {query}
Analysis:
"""

second_template = """
As a professional financial advisor at a bank, your goal is to provide tailored recommendations that align with the customer's financial situation and goals.
Using the customer analysis provided and the available banking products, determine the most suitable product(s) for this customer.
Please explain why this product is the best fit, considering the customer's financial needs, potential risks, and long-term benefits.
Customer Analysis: {customer_analysis}
Available Products: {product_info}
Recommendation:
"""

# Initialize model and prompts for existing customers
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

first_prompt = PromptTemplate(input_variables=["query"], template=first_template)
second_prompt = PromptTemplate(input_variables=["customer_analysis", "product_info"], template=second_template)

first_chain = LLMChain(llm=model, prompt=first_prompt, output_key="customer_analysis", verbose=True)
second_chain = LLMChain(llm=model, prompt=second_prompt, output_key="final_recommendation", verbose=True)

sequential_chain = SequentialChain(
    chains=[first_chain, second_chain],
    input_variables=["query", "product_info"],
    output_variables=["final_recommendation"]
)

# Define new prompt templates for new users (prospective customers)
new_user_first_template = """
You are a seasoned financial advisor at a bank. A prospective customer, who is new to our bank, has provided their financial details and bank statement information.
Analyze the following customer data and extract key financial insights, potential needs, and any risks that might affect their financial stability.
Customer Data: {query}
Analysis:
"""

new_user_second_template = """
Based on the above analysis and the bank's available product offerings, recommend the most suitable product(s) for the prospective customer.
Explain why the recommended product(s) fit the customer's unique financial situation and long-term goals.
Customer Analysis: {customer_analysis}
Available Products: {product_info}
Recommendation:
"""

# Initialize prompts and chains for new users
new_user_first_prompt = PromptTemplate(input_variables=["query"], template=new_user_first_template)
new_user_second_prompt = PromptTemplate(input_variables=["customer_analysis", "product_info"], template=new_user_second_template)

new_user_first_chain = LLMChain(llm=model, prompt=new_user_first_prompt, output_key="customer_analysis", verbose=True)
new_user_second_chain = LLMChain(llm=model, prompt=new_user_second_prompt, output_key="final_recommendation", verbose=True)

new_user_sequential_chain = SequentialChain(
    chains=[new_user_first_chain, new_user_second_chain],
    input_variables=["query", "product_info"],
    output_variables=["final_recommendation"]
)

# Define the route to get all customer IDs
@app.get("/customers")
async def get_customer_ids():
    if not customer_dataset:
        raise HTTPException(status_code=500, detail="Customer data not available")
    
    customer_ids = [customer["CustomerID"] for customer in customer_dataset]
    return {"customer_ids": customer_ids}

# Define the route to generate recommendations for existing customers
@app.post("/recommendation")
async def generate_recommendation(customer_id: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Vector database not initialized")
    
    retriever = db.as_retriever(search_kwargs={"k": 1})
    retrieved_documents = retriever.get_relevant_documents(customer_id)
    
    if not retrieved_documents:
        logger.warning(f"Customer ID {customer_id} not found in FAISS.")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer_info = "\n".join([doc.page_content for doc in retrieved_documents])
    
    product_info = "\n".join(
        [f"Name: {prod['name']}, Category: {prod['category']}, Features: {prod['features']}, Description: {prod['description']}" 
         for prod in product_dataset]
    )
    
    logger.info(f"Generating recommendation for Customer ID: {customer_id}")
    result = sequential_chain({"query": customer_info, "product_info": product_info})
    
    return {"recommendation": result["final_recommendation"]}

# Define the route to generate recommendations for new (prospective) users
@app.post("/recommendation/new_user")
async def generate_recommendation_for_new_user(customer_data: dict):
    """
    Generate a recommendation for a new user (not in MySQL).
    Accepts financial details and extracted text from a bank statement.
    """
    if not customer_data:
        raise HTTPException(status_code=400, detail="Customer data is required")

    try:
        # Convert customer data to a formatted JSON string
        customer_info = json.dumps(customer_data, indent=4)

        # Prepare product data string
        product_info = "\n".join(
            [f"Name: {prod['name']}, Features: {prod['features']}, Description: {prod['description']}" 
             for prod in product_dataset]
        )

        logger.info("Generating recommendation for new user...")
        result = new_user_sequential_chain({"query": customer_info, "product_info": product_info})

        return {"recommendation": result["final_recommendation"]}
    
    except Exception as e:
        logger.error(f"❌ Error processing new user recommendation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting FastAPI server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
