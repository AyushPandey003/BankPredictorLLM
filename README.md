# BankLLM Project

This project aims to build a bank product recommendation system using LangChain.  It leverages a MySQL database for customer and product data, and utilizes LangChain's capabilities for creating a recommendation engine.

## Project Structure

The project is organized as follows:

- **src/:** Contains the source code and data files.
    - **app.py:** Main FastAPI application for generating recommendations using Google Generative AI.
    - **app2.py:** Alternative FastAPI application for generating recommendations using OpenAI.
    - **client.py:** Streamlit client for interacting with the API.
    - **config.py:** Configuration file for database and API keys.
    - **customer_profile.json:** JSON file containing customer data (loaded from MySQL).
    - **db_connect.py:** Module for connecting to and fetching data from the MySQL database.
    - **products.json:** JSON file containing product data (loaded from MySQL).
    - **requestsop.py:**  A script for downloading files from public URLs (currently unused in the main application).
    - **requirements.txt:** List of project dependencies.
    - **unlockPassword.py:** Script for removing password protection from a PDF file (currently unused in the main application).
    - **.env:** Environment variables for database credentials and API keys.

- **data/:** Contains data files used for development and testing.
- **docs/:** Contains documentation and screenshots.


## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r src/requirements.txt
   ```

2. **Configure Database:**
   - Create a MySQL database named `defaultdb` (or change the `MYSQL_DB` variable in `.env`).
   - Create tables named `CustomerProfile` and `Products` in the database.  Populate these tables with the data provided in `src/customer_profile.json` and `src/products.json` respectively.  You may need to adjust the schema to match your data.
   - Update the database credentials in the `.env` file.

3. **Set API Keys:**
   - Obtain API keys for Google Generative AI and OpenAI (if using app2.py).
   - Set the `LANGCHAIN_API_KEY` and `OPENAI_API_KEY` environment variables in the `.env` file.

4. **Run the Application:**
   - To run the application using Google Generative AI, execute:
     ```bash
     python src/app.py
     ```
   - To run the application using OpenAI, execute:
     ```bash
     python src/app2.py
     ```

5. **Run the Streamlit Client:**
   ```bash
   streamlit run src/client.py
   ```

## Usage

The Streamlit client provides a user interface for selecting a customer ID and generating a product recommendation.  For new users, it allows manual input of financial details and bank statement upload for OCR processing.

## Notes

- The `requestsop.py` and `unlockPassword.py` files are currently not integrated into the main application.
- Error handling is implemented to gracefully handle database connection and data loading issues.
- The application uses LangChain to build a recommendation engine based on customer data and available products.
