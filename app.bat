call venv/Scripts/activate

call uvicorn src.main:app --reload --port 8080

pause
