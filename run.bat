@echo off
title Autonomous Research AI

cd /d D:\autonomous_research_ai

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting Ollama...
start cmd /k ollama serve

timeout /t 5 /nobreak >nul

echo Starting Streamlit App...
start cmd /k streamlit run app.py --server.headless true --browser.gatherUsageStats false

exit
