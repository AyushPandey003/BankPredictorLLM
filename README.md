# Bank Product Recommendation System

This project is an AI-powered bank product recommendation system that provides tailored financial product suggestions to both existing and new bank customers. It uses a FastAPI backend with LangChain for the core logic and a Streamlit frontend for the user interface.

## Features

- **Existing Customer Recommendations**: Existing customers can select their customer ID to receive personalized product recommendations based on their financial history.
- **New Customer Recommendations**: New customers can input their financial details (income, age, credit score, etc.) and upload a bank statement to receive product recommendations.
- **AI-Powered Analysis**: The system uses a Large Language Model (LLM) to analyze customer data and provide insightful recommendations.
- **Modern UI**: The user interface is built with Streamlit and is designed to be user-friendly and intuitive.

## Tech Stack

- **Backend**: FastAPI, LangChain, Google Generative AI
- **Frontend**: Streamlit
- **Database**: MySQL (for customer and product data)
- **Data Handling**: Pandas, SQLAlchemy
- **Deployment**: Docker (optional)

## Project Structure

```
BankLLM/
├── data/                 # Sample data and SQL scripts
├── docs/                 # Project documentation and images
├── src/                  # Source code
│   ├── app.py            # FastAPI backend
│   ├── client.py         # Streamlit frontend
│   ├── config.py         # Configuration file
│   ├── db_connect.py     # Database connection logic
│   ├── requirements.txt  # Python dependencies
│   └── ...
├── .gitignore
├── pyproject.toml        # Project metadata and dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- MySQL Server
- Tesseract OCR (for bank statement text extraction)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/BankLLM.git
   cd BankLLM
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r src/requirements.txt
   ```

3. **Set up the database:**
   - Create a MySQL database.
   - Run the SQL scripts in the `data/` directory to create the necessary tables and insert sample data.

4. **Configure the application:**
   - Rename `.env.example` to `.env` and update the environment variables with your database credentials and API keys.

### Running the Application

1. **Start the FastAPI backend:**
   ```bash
   uvicorn src.app:app --reload
   ```
   The backend will be available at `http://127.0.0.1:8000`.

2. **Run the Streamlit frontend:**
   ```bash
   streamlit run src/client.py
   ```
   The frontend will be available at `http://localhost:8501`.

## Usage

- **Existing Customers**: Select your customer ID from the dropdown and click "Get Recommendation".
- **New Customers**: Fill in your financial details and optionally upload a bank statement, then click "Generate Recommendation".

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.