@echo off

REM Change directory to 'src'
cd /d D:\BankLLM\src

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start FastAPI server with uvicorn
start uvicorn app:app --reload

REM Start Streamlit app
start streamlit run client.py

REM Pause (optional, to keep the command window open)
pause
